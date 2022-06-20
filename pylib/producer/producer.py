from typing import List, Callable, Any, Optional, Union, Set, Tuple, TypeVar, Generic, Dict, TypedDict
from dataclasses import dataclass
import re
import sqlite3


# def core_categories(input_files: InputFileDatatype) -> List[str]:
#     return ["core", input_files["input"]]


# def core_resource_paths(input_files: Input_fileDatatype, grouping_values: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]
# def core_resource_paths(index: int, regex: str, match: re.Match) -> Tuple[InputFileDatatype, OutputFileDatatype]:
#     return ({
#             "input": match.group(0)
#         },{
#             "output": os.path.join("output", os.path.basename(match.group(0)))
#         })
    
# def producer_copyfile(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:



InputFileDatatype = TypeVar("InputFileDatatype", bound=TypedDict)
OutputFileDatatype = TypeVar("OutputFileDatatype", bound=TypedDict)

@dataclass(init=False)
class Producer(Generic[InputFileDatatype, OutputFileDatatype]):
    # A list of file regex matches. If a file is changed that matches one of
    # these regex matches then this producer will trigger 
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
    # self_watch_function: Optional[Callable[], Any]ff


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
        for field_index, field_name in enumerate(input_path_patterns):
            self._field_to_index[field_name] = field_index

        # A map between each unique group in the field and a unique integer that
        # is guarenteed to be a safe sql name.
        self._regex_group_to_index: Dict[str, int] = {}
        all_regex_groups: Set[str] = set()


        # Preprocess all the regex data
        for field_name, field_pattern in input_path_patterns.items():
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
            self._compiled_regexes[field_name] =  field_regex

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


    def regex_field_patterns(self) -> Dict[str, "re.Pattern[str]"]:
        return self._compiled_regexes


    @staticmethod
    def get_field_table_name(producer_index: int, field_index: int) -> str:
        return "producer{producer_index}_field{field_index}_matches".format(producer_index=producer_index, field_index=field_index)


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


    def query_filesets(self, db: sqlite3.Connection, producer_index: int) -> List[Tuple[InputFileDatatype, Dict[str,str]]]:
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

        for field_name in self._input_path_patterns:
            if self._input_path_patterns[field_name] == "":
                continue
            elif self._input_path_patterns[field_name] == []:
                continue

            field_index = self._field_to_index[field_name]
            field_query_index[field_name] = len(fields)

            table_name = Producer.get_field_table_name(producer_index=producer_index, field_index=field_index)

            if isinstance(self._input_path_patterns[field_name], str):
                singleton_fields.append(table_name + ".filename")
                fields.append(table_name+".filename")

            # If the field is a list then we want to grab each file and put it into a list
            # this is done by using
            elif isinstance(self._input_path_patterns[field_name], list):
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

        query_string = "SELECT {fields} FROM {field_tables} WHERE {field_joins} GROUP BY {singleton_fields};".format(
            fields=", ".join(fields),
            field_tables=", ".join(tables),
            field_joins=" AND ".join(field_joins),
            singleton_fields=", ".join(singleton_fields)
        )

        # print(query_string)
        output_data: List[Tuple[InputFileDatatype, Dict[str,str]]] = []
        with db:
            cur = db.execute(
                query_string,
            )


            for row in cur.fetchall():

                new_element: InputFileDatatype = {} #= self._input_path_patterns.copy()
                groups: Dict[str, str] = {}

                for new_element_field, pattern in self._input_path_patterns.items():
                    if pattern == "":
                        new_element[new_element_field] = "" # type:ignore
                        continue
                    elif pattern == []:
                        new_element[new_element_field] = [] # type:ignore
                        continue

                    value:str = row[field_query_index[new_element_field]]                    
                    if isinstance(pattern, str):
                        new_element[new_element_field] = value # type:ignore
                    elif isinstance(pattern, list):
                        new_element[new_element_field] = sorted(parse_comma_escape(value)) # type:ignore
                    else:
                        raise TypeError()

                for group in group_query_index:
                    groups[group] = row[group_query_index[group]]


                output_data.append((new_element, groups))


        return output_data


    ############################################################################
    # insert
    #
    # Insert a file for this producer into the database
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

        fields = ["filename"] + [ "group_{}".format(self._regex_group_to_index[x]) for x in groups.keys() ]

        binds = [filename] + list(groups.values())

        query_string: str = "INSERT INTO {table} ({fields}) VALUES ({value_binds})".format(
                table=table,
                fields=", ".join(fields),
                value_binds=", ".join("?" * len(fields))
            )

        # print(query_string, binds)

        with db:
            db.execute(
                query_string,
                binds,
            )



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

