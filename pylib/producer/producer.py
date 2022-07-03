from dataclasses import dataclass
from typing import List, Callable, Any, Union, Set, Tuple, TypeVar, Generic, Dict, TypedDict, Iterable
import re
import sqlite3

# TODO: mypy does not like bound=TypedDict while pyright says it is ok
# InputFileDatatype = TypeVar("InputFileDatatype", bound="TypedDict")
InputFileDatatype = TypeVar("InputFileDatatype", bound=Iterable[Any])
# TODO: mypy does not like bound=TypedDict while pyright says it is ok
# OutputFileDatatype = TypeVar("OutputFileDatatype", bound="TypedDict")
OutputFileDatatype = TypeVar("OutputFileDatatype", bound=Iterable[Any])


################################################################################
# Producer
#
# An object that represents a set of rules for generating an ouput file from
# one or more input files.
################################################################################
@dataclass(init=False)
class Producer(Generic[InputFileDatatype, OutputFileDatatype]):
    # A list of file regex matches. If a file is changed that matches one of
    # these regex matches then this producer will trigger.
    _input_path_patterns: InputFileDatatype

    # A function that takes in the matching input pattern and generates a set
    # of input and output files.
    paths: Callable[[InputFileDatatype, Dict[str, str]], Tuple[InputFileDatatype, OutputFileDatatype]]

    # A function that takes in the input and output files and performs the
    # tasks required to transform the input files into output files.
    function: Callable[[InputFileDatatype, OutputFileDatatype], None]

    # A list of tags or a function that generates tags based on input and output data
    categories: Union[List[str], Callable[[InputFileDatatype, OutputFileDatatype], List[str]]]

    # an alternative for "function" that will be called if this step is to be skipped
    # EG: javascript minification would have a simple copyfunction here because
    #     the file(s) still need to exist at the destination.
    # fast_function: Optional[Callable[[InputFileDatatype, OutputFileDatatype], None]] = None

    # # A function that handles its own monitoring and updating logic. For example
    # # the `tsc` typescript compiler.
    # self_watcher_function: Optional[Callable[[], Any]]

    # To take advantage of hot retriggering of some expensive-to-start javascript commands like tsc
    # self_watch_function: Optional[Callable[], Any]

    # A map of pre-compiled regexes that map to the InputFileDatatype keys
    # Python apparently cannot handle Dict[str, List[re.Pattern[str]]] here
    _compiled_regexes: Dict[str, "re.Pattern[str]"]

    # Map of all the join groups that are present for each key of InputFileDatatype
    _regex_groups: Dict[str, List[str]]

    def __init__(
        self,
        input_path_patterns: InputFileDatatype,
        paths: Callable[[InputFileDatatype, Dict[str, str]], Tuple[InputFileDatatype, OutputFileDatatype]],
        function: Callable[[InputFileDatatype, OutputFileDatatype], None],
        categories: Union[List[str], Callable[[InputFileDatatype, OutputFileDatatype], List[str]]],
    ):
        self._input_path_patterns = input_path_patterns
        self.paths = paths
        self.function = function
        self.categories = categories
        self._compiled_regexes = {}
        self._regex_groups = {}

        # A map between each field name and a unique integer that is guarenteed
        # to be a safe sql name.
        self._field_to_index: Dict[str, int] = {}
        field_name: str
        for field_index, field_name in enumerate(input_path_patterns):
            self._field_to_index[field_name] = field_index

        # A map between each unique group in the field and a unique integer that
        # is guarenteed to be a safe sql name.
        self._regex_group_to_index: Dict[str, int] = {}
        all_regex_groups: Set[str] = set()

        # Preprocess all the regex data
        # mypy yells at using .items() on a typed dict even though it is a dict
        for field_name, field_pattern in input_path_patterns.items():  # type:ignore
            field_regex: re.Pattern[str]

            if isinstance(field_pattern, str):
                if field_pattern == "":
                    continue

                field_regex = re.compile(field_pattern)
            elif isinstance(field_pattern, list):
                if len(field_pattern) == 0:
                    continue
                if len(field_pattern) > 1:
                    raise TypeError
                field_regex = re.compile(field_pattern[0])
            else:
                raise TypeError("InputFileDatatype must be a dict of only str or List[str]. Found an element of type " + str(type(field_pattern)))

            # Save a cache of the compiled regexes for easier access.
            self._compiled_regexes[field_name] = field_regex

            # Save the list of different regex groups to join on for this key.
            field_regex_groups: Set[str] = set()
            for group_name in field_regex.groupindex:
                field_regex_groups.add(group_name)
                all_regex_groups.add(group_name)

            self._regex_groups[field_name] = list(field_regex_groups)

        # Populate a map between each unique group in the field and a unique
        # integer that is guarenteed to be a safe sql name.
        for group_index, group_name in enumerate(sorted(list(all_regex_groups))):
            self._regex_group_to_index[group_name] = group_index

    ############################################################################
    # regex_field_patterns
    #
    # A helper function to return the dict cache of compiled regexess that this
    # producer uses.
    ############################################################################
    def regex_field_patterns(self) -> Dict[str, "re.Pattern[str]"]:
        return self._compiled_regexes

    ############################################################################
    # get_field_table_name
    #
    # A helper function to produce the name of the table that stores matches
    # for a particular field.
    # TODO: The SQL logic should somehow be moved to scheduler.py
    ############################################################################
    @staticmethod
    def get_field_table_name(producer_index: int, field_index: int) -> str:
        return "producer{producer_index}_field{field_index}_matches".format(producer_index=producer_index, field_index=field_index)

    ############################################################################
    # init_table_query
    #
    # Create a series of sql query strings that are used to create all of the
    # tables for each field in this producer.
    # TODO: The SQL logic should somehow be moved to scheduler.py
    ############################################################################
    def init_table_query(self, producer_index: int) -> List[str]:

        query_strings: List[str] = []

        # NO fucking idea if this is done or not or if this is even a sane direction
        # we should probably use best practices even though sql injection is not an issue here (yet)

        for field_name in self.regex_field_patterns():

            field_index = self._field_to_index[field_name]

            table_columns: List[str] = ["filename TEXT"]

            for group_name in self._regex_groups[field_name]:
                table_columns.append("group_{} TEXT".format(self._regex_group_to_index[group_name]))

            field_table_name = Producer.get_field_table_name(producer_index=producer_index, field_index=field_index)
            query_string = "CREATE TABLE {field_table_name} (".format(field_table_name=field_table_name)

            query_string += ", ".join(table_columns)

            query_string += ");"

            query_strings.append(query_string)

        return query_strings

    ############################################################################
    # query_filesets
    #
    # Query all of the valid combinations of files that can be used for this
    # producer using the field matches that have been stored in the database.
    # TODO: The SQL logic should somehow be moved to scheduler.py
    ############################################################################
    def query_filesets(self, db: sqlite3.Connection, producer_index: int) -> List[Tuple[InputFileDatatype, Dict[str, str]]]:
        # A list of fields to SELECT from. These should corrispond exactly to
        # every non-empty field in the InputFieldDatatype.
        fields: List[str] = []

        # A way to lookup which sql result to use for each field in InputFileDatatype
        field_query_index: Dict[str, int] = {}

        # A way to lookup which sql result to use for each group for the regex results of InputFileDatatype
        group_query_index: Dict[str, int] = {}

        # A list of tables to select FROM. These should corrispond exactly to
        # every non-empty field in the InputFieldDatatype.
        tables: List[str] = []

        # A list of feilds that will be GROUP BY'ed in order to merge list
        # fields into a single row so they can be accurately inserted into
        # the InputFileDatatype.
        singleton_fields: List[str] = []

        # A map of each group to the list of tables that group is in
        field_groups: Dict[str, List[str]] = {}

        # mypy complains about iterating over a typeddict even though it is a dict
        for field_name, field in self._input_path_patterns.items():  # type: ignore
            if field == "":
                continue
            elif field == []:
                continue

            field_index = self._field_to_index[field_name]
            field_query_index[field_name] = len(fields)

            table_name = Producer.get_field_table_name(producer_index=producer_index, field_index=field_index)

            if isinstance(field, str):
                singleton_fields.append(table_name + ".filename")
                fields.append(table_name + ".filename")

            # If the field is a list then we want to grab each file and put it into a list
            # this is done by using
            elif isinstance(field, list):
                fields.append("GROUP_CONCAT(REPLACE(REPLACE({table_name}.filename, '\\','\\\\'), ',', '\\,'), ',')".format(table_name=table_name))
            else:
                raise TypeError("Expected either a str or a list")

            tables.append(table_name)

            for field_group in self._regex_groups[field_name]:
                if field_group not in field_groups:
                    field_groups[field_group] = []

                field_groups[field_group].append(table_name)

        field_joins: List[str] = []
        for field_group, group_tables in field_groups.items():
            first_table = group_tables[0]
            group_index = self._regex_group_to_index[field_group]

            group_query_index[field_group] = len(fields)
            singleton_fields.append("{first_table}.group_{group_index}".format(first_table=first_table, group_index=group_index))
            fields.append("{first_table}.group_{group_index}".format(first_table=first_table, group_index=group_index))

            for table in group_tables[1:]:
                field_joins.append("{first_table}.group_{group_index} = {table}.group_{group_index}".format(
                    first_table=first_table,
                    group_index=group_index,
                    table=table,
                ))

        # Prevent the WHERE clause from being blank ever.
        # TODO: The WERE clause should probably just be removed entirely but the
        # query is already imperfect by not using JOINs instead so this will be
        # left until we re-evaluate the query again.
        if len(field_joins) == 0:
            field_joins = ["1=1"]

        query_string = "SELECT {fields} FROM {field_tables} WHERE {field_joins} GROUP BY {singleton_fields};".format(
            fields=", ".join(fields),
            field_tables=", ".join(tables),
            field_joins=" AND ".join(field_joins),
            singleton_fields=", ".join(singleton_fields)
        )

        output_data: List[Tuple[InputFileDatatype, Dict[str, str]]] = []
        with db:
            cur = db.execute(
                query_string,
            )

            for row in cur.fetchall():

                new_element: InputFileDatatype = {}  # type:ignore
                groups: Dict[str, str] = {}

                for new_element_field, pattern in self._input_path_patterns.items():  # type: ignore
                    if pattern == "":
                        new_element[new_element_field] = ""  # type:ignore
                        continue
                    elif pattern == []:
                        new_element[new_element_field] = []  # type:ignore
                        continue

                    value: str = row[field_query_index[new_element_field]]
                    if isinstance(pattern, str):
                        new_element[new_element_field] = value  # type:ignore
                    elif isinstance(pattern, list):
                        new_element[new_element_field] = sorted(parse_comma_escape(value))  # type:ignore
                    else:
                        raise TypeError()

                for group in group_query_index:
                    groups[group] = row[group_query_index[group]]

                output_data.append((new_element, groups))

        return output_data

    ############################################################################
    # insert
    #
    # Insert a file that has matched a field for this producer into the
    # database table for that field.
    # TODO: The SQL logic should somehow be moved to scheduler.py
    ############################################################################
    def insert(
        self,
        db: sqlite3.Connection,
        producer_index: int,
        field_name: str,
        filename: str,
        groups: Dict[str, str]
    ) -> None:
        field_index = self._field_to_index[field_name]

        table = Producer.get_field_table_name(producer_index=producer_index, field_index=field_index)

        fields = ["filename"] + ["group_{}".format(self._regex_group_to_index[x]) for x in groups.keys()]

        binds = [filename] + list(groups.values())

        query_string: str = "INSERT INTO {table} ({fields}) VALUES ({value_binds})".format(
            table=table,
            fields=", ".join(fields),
            value_binds=", ".join("?" * len(fields))
        )

        with db:
            db.execute(
                query_string,
                binds,
            )


################################################################################
# parse_comma_escape
#
# Parses the escaped comma string returned from the SQL query back into an
# array. The query escapes all backslashes and commas, then uses a comma to
# delimite each element in the array.
# TODO: The SQL logic should somehow be moved to scheduler.py
################################################################################
def parse_comma_escape(input_string: str) -> List[str]:
    output_strings: List[str] = [""]
    last_character: str = ""
    for character in input_string:
        if character == "," and last_character != "\\":
            output_strings.append("")
        elif character == "\\" and last_character != "\\":
            pass
        else:
            output_strings[-1] += character

        last_character = character

    return output_strings


# Convenience type to get around making lists of Producers with different
# arguments.
GenericProducer = Producer[Any, Any]
