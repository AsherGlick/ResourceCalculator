from .producer import GenericProducer
from typing import List, Tuple, Any, Dict, Union
import sqlite3

MatchGroups = Dict[str, str]
InputArguments = Any


class FileSet:
    producer_list: List[GenericProducer] = []

    def __init__(self, producer_list: List[GenericProducer]):
        raise NotImplementedError

    def add_file(
        self,
        producer_index: int,  # why do we need this?
        field_name: str,  # what does this do?
        filename: str,
        groups: Dict[str, str],
    ) -> None:
        raise NotImplementedError

    def remove_file(
        self,
        producer_index: int,  # why do we need this?
        field_name: str,  # what does this do?
        filename: str,
    ) -> None:
        raise NotImplementedError

    def query_filesets(self, producer_index: int) -> List[Tuple[InputArguments, MatchGroups]]:
        raise NotImplementedError


############################################################################
############################################################################
# SQL LOGIC
############################################################################
############################################################################
class SqlFileSet(FileSet):
    db: sqlite3.Connection

    def __init__(self, producer_list: List[GenericProducer]):
        self.producer_list = producer_list
        self.db = self._init_fileset_database(producer_list)

    def add_file(
        self,
        producer_index: int,
        field_name: str,
        filename: str,
        groups: Dict[str, str],
    ) -> None:
        return self._insert_file_into_database(self.db, producer_index, field_name, filename, groups)

    def remove_file(
        self,
        producer_index: int,
        field_name: str,
        filename: str,
    ) -> None:
        return self._remove_file_from_database(self.db, producer_index, field_name, filename)

    def query_filesets(self, producer_index: int) -> List[Tuple[InputArguments, MatchGroups]]:
        return self._query_filesets_from_database(self.db, producer_index)

    ############################################################################
    # _init_fileset_database
    #
    # Create the cache database for storing all the files that match a producer
    # field, and then initialize all of the tables in the database.
    # file instead.
    ############################################################################
    def _init_fileset_database(self, producer_list: List[GenericProducer]) -> sqlite3.Connection:
        db = sqlite3.connect(':memory:')

        for producer_index, producer in enumerate(producer_list):
            for init_query in self._init_fileset_database_sql(producer_index):
                with db:
                    db.execute(init_query)

        return db

    ############################################################################
    # _init_fileset_database_sql
    #
    # Create a series of sql query strings that are used to create all of the
    # tables for each field in this producer.
    ############################################################################
    def _init_fileset_database_sql(self, producer_index: int) -> List[str]:
        producer: GenericProducer = self.producer_list[producer_index]

        query_strings: List[str] = []

        for field_name in producer.regex_field_patterns():

            field_id: str = producer.get_field_id(field_name)

            field_table_name = _get_field_table_name(
                producer_index=producer_index,
                field_id=field_id
            )

            table_columns: List[str] = [
                "filename TEXT UNIQUE",
            ]

            for group_name in producer.get_match_groups(field_name):
                table_columns.append(_get_match_group_column_name(
                    producer=producer,
                    group_name=group_name,
                ) + " TEXT")

            query_string = "CREATE TABLE {field_table_name} ({table_columns});".format(
                field_table_name=field_table_name,
                table_columns=", ".join(table_columns)
            )

            query_strings.append(query_string)

        return query_strings

    ############################################################################
    # _insert_file_into_database
    #
    # Insert a file that has matched a field for this producer into the
    # database table for that field.
    ############################################################################
    def _insert_file_into_database(
        self,
        db: sqlite3.Connection,
        producer_index: int,
        field_name: str,
        filename: str,
        groups: Dict[str, str]
    ) -> None:
        query_string, binds = self._insert_file_into_database_sql(
            producer_index=producer_index,
            field_name=field_name,
            filename=filename,
            groups=groups
        )

        with db:
            db.execute(
                query_string,
                binds,
            )

    def _insert_file_into_database_sql(
        self,
        producer_index: int,
        field_name: str,
        filename: str,
        groups: Dict[str, str]
    ) -> Tuple[str, List[str]]:
        producer = self.producer_list[producer_index]
        field_id = producer.get_field_id(field_name)
        table_name = _get_field_table_name(producer_index=producer_index, field_id=field_id)

        fields = ["filename"] + [_get_match_group_column_name(producer=producer, group_name=group_name) for group_name in groups.keys()]

        binds: List[str] = [filename] + list(groups.values())

        query_string: str = "INSERT INTO {table} ({fields}) VALUES ({value_binds})".format(
            table=table_name,
            fields=", ".join(fields),
            value_binds=", ".join("?" * len(fields))
        )

        return query_string, binds

    def _remove_file_from_database(
        self,
        db: sqlite3.Connection,
        producer_index: int,
        field_name: str,
        filename: str,
    ) -> None:

        query_string = self._remove_file_from_database_sql(producer_index, field_name)
        with db:
            db.execute(
                query_string,
                {
                    "filename": filename
                },
            )

    def _remove_file_from_database_sql(
        self,
        producer_index: int,
        field_name: str,
    ) -> str:

        producer = self.producer_list[producer_index]
        table_name = _get_field_table_name(
            producer_index=producer_index,
            field_id=producer.get_field_id(field_name)
        )
        query_string: str = "DELETE FROM {table} WHERE filename = :filename".format(
            table=table_name
        )

        return query_string

    ############################################################################
    # query_filesets
    #
    # Query all of the valid combinations of files that can be used for this
    # producer using the field matches that have been stored in the database.
    ############################################################################
    def _query_filesets_from_database(
        self,
        db: sqlite3.Connection,
        producer_index: int
        # TODO: once we figure out how to better handle the types internally in
        #   this tool we should get rid of the "Any" here and replace it with a
        #   real type.
        # List[Tuple[InputFileDatatype, Dict[str, str]]]:
    ) -> List[Tuple[Any, Dict[str, str]]]:
        query_string = self._query_filesets_from_database_sql(producer_index)

        producer = self.producer_list[producer_index]

        # output_data: List[Tuple[InputFileDatatype, Dict[str, str]]] = []
        output_data: List[Tuple[Any, Dict[str, str]]] = []
        with db:
            cur = db.execute(
                query_string,
            )

            columns = [x[0] for x in cur.description]
            columns_lookup = {value: index for index, value in enumerate(columns)}

            for row in cur.fetchall():

                new_element: Dict[str, Union[str, List[str]]] = {}
                groups: Dict[str, str] = {}

                for new_element_field_name, pattern in producer.input_path_patterns_dict().items():
                    new_element_field_id = producer.get_field_id(new_element_field_name)
                    if pattern == "":
                        new_element[new_element_field_name] = ""
                        continue
                    elif pattern == []:
                        new_element[new_element_field_name] = []
                        continue

                    value: str = row[columns_lookup["field_" + new_element_field_id]]
                    if isinstance(pattern, str):
                        new_element[new_element_field_name] = value
                    elif isinstance(pattern, list):
                        new_element[new_element_field_name] = sorted(parse_comma_escape(value))
                    else:
                        raise TypeError()

                for group_name in producer.get_all_match_groups():
                    group_id = producer.get_match_group_id(group_name)
                    groups[group_name] = row[columns_lookup["group_" + group_id]]

                output_data.append((new_element, groups))

        return output_data

    def _query_filesets_from_database_sql(self, producer_index: int) -> str:
        producer = self.producer_list[producer_index]

        # A list of columns to select. Should end up as the union between
        # every field and every match group
        columns: List[str] = []

        # A list of tables to select FROM. These should corrispond exactly to
        # every non-empty field in the InputFieldDatatype.
        tables: List[str] = []

        # A list of columns that will be GROUP BY'ed in order to merge list
        # fields into a single row so they can be accurately inserted into
        # the InputFileDatatype.
        group_by_columns: List[str] = []

        # A map of each group to the list of tables that group is in
        field_groups: Dict[str, List[str]] = {}

        field_wheres: List[str] = []

        # mypy complains about iterating over a typeddict even though it is a dict
        for field_name, field_value in producer.input_path_patterns_dict().items():
            if field_value == "":
                continue
            elif field_value == []:
                continue

            field_id = producer.get_field_id(field_name)

            table_name = _get_field_table_name(
                producer_index=producer_index,
                field_id=field_id
            )

            table_contents = table_name

            field_alias = "\"field_{field_id}\"".format(
                field_id=field_id,
            )

            if isinstance(field_value, str):
                columns.append("{table_name}.filename AS {field_alias}".format(
                    table_name=table_name,
                    field_alias=field_alias,
                ))
                group_by_columns.append(str(len(columns)))

            # If the field is a list then we want to grab each file and put it into a list
            # this is done by using
            elif isinstance(field_value, list):
                match_columns = [_get_match_group_column_name(producer, match_group) for match_group in producer.get_match_groups(field_name)]
                new_table_name = table_name + "_mod"

                table_contents = "(SELECT GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename, {match_columns} FROM {table_name} GROUP BY {match_columns}) as {new_table_name}".format(
                    table_name=table_name,
                    new_table_name=new_table_name,
                    match_columns=", ".join(match_columns)
                )

                columns.append("GROUP_CONCAT({table_name}.filename, ',') AS {field_alias}".format(
                    table_name=new_table_name,
                    field_alias=field_alias,
                ))

                table_name = new_table_name

            else:
                raise TypeError("Expected either a str or a list")

            tables.append(table_contents)

            for match_group_name in producer.get_match_groups(field_name):
                if match_group_name not in field_groups:
                    field_groups[match_group_name] = []

                field_groups[match_group_name].append(table_name)

        field_joins: List[str] = []
        for match_group_name, group_tables in field_groups.items():
            first_table = group_tables[0]

            columns.append("{first_table}.{group_column_name}".format(
                first_table=first_table,
                group_column_name=_get_match_group_column_name(producer, match_group_name)
            ))
            group_by_columns.append(str(len(columns)))

            for table in group_tables[1:]:
                field_joins.append("{first_table}.{group_column_name} = {table}.{group_column_name}".format(
                    first_table=first_table,
                    group_column_name=_get_match_group_column_name(producer, match_group_name),
                    table=table,
                ))

        # Prevent the WHERE clause from being blank ever.
        # TODO: The WERE clause should probably just be removed entirely but the
        # query is already imperfect by not using JOINs instead so this will be
        # left until we re-evaluate the query again.
        if len(field_joins) == 0:
            field_joins = ["1=1"]

        query_string = "SELECT {columns} FROM {field_tables} WHERE {field_wheres} GROUP BY {group_by_columns};".format(
            columns=", ".join(columns),
            field_tables=", ".join(tables),
            field_wheres=" AND ".join(field_wheres + field_joins),
            group_by_columns=", ".join(group_by_columns)
        )

        return query_string


################################################################################
# parse_comma_escape
#
# Parses the escaped comma string returned from the SQL query back into an
# array. The query escapes all backslashes and commas, then uses a comma to
# delimite each element in the array.
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


################################################################################
# get_field_table_name
#
# A helper function to produce the name of the table that stores matches
# for a particular field.
################################################################################
def _get_field_table_name(producer_index: int, field_id: str) -> str:
    return "producer{producer_index}_field{field_id}_matches".format(
        producer_index=producer_index,
        field_id=field_id
    )


################################################################################
# get_match_group_column_name
#
# A helper function to produce the name of the column that corrisponds to a
# particular named regex match group.
################################################################################
def _get_match_group_column_name(producer: GenericProducer, group_name: str) -> str:
    return "group_{group_id}".format(
        group_id=producer.get_match_group_id(group_name)
    )
