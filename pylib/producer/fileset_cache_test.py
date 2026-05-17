import unittest
from typing import Dict, List, Any, Union
from dataclasses import dataclass
import re

from .fileset_cache import SqlFileSet
from .producer import Producer


# Simple dummy function for the producers because they will never be used
def dummy_function(input_files: Any, groups: Dict[str, str]) -> List[str]:
    return ["output_file"]  # pragma: nocover


def reduce_whitespace(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\(\s+', '(', text)
    text = re.sub(r'\s+\)', ')', text)
    return text.strip()


@dataclass
class SQLQueryTestcase:
    test_name: str

    input_path_patterns: Dict[str, Union[str, List[str]]]
    test_fieldname: str

    init_tables_sql: List[str]

    insert_file_sql: str
    insert_file_filename: str
    insert_file_groups: Dict[str, str]
    insert_file_sql_binds: List[str]

    # remove_file_sql: str

    query_filesets_sql: str


class TestSQLFileSet(unittest.TestCase):
    maxDiff = 9999999

    def test_sql_queries(self) -> None:
        cases: List[SQLQueryTestcase] = [
            # SQLQueryTestcase(
            #     test_name="",
            #     input_path_patterns={},
            #     test_fieldname="",
            #     init_tables_sql=[],
            #     insert_file_filename="",
            #     insert_file_groups={},
            #     insert_file_sql="",
            #     insert_file_sql_binds=[],
            #     query_filesets_sql="",
            # ),
            # singlefile ###############################################################################################
            SQLQueryTestcase(
                test_name="single_file_with_no_groups",
                input_path_patterns={
                    "file": r"file"
                },
                test_fieldname="file",
                init_tables_sql=[
                    reduce_whitespace("""
                        CREATE TABLE producer0_field0_matches (
                            filename TEXT UNIQUE,
                            group_0 TEXT
                        );
                    """),
                ],
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_filename="rndm_filename",
                insert_file_groups={"__file": "rndm_group_value"},
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],

                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        producer0_field0_matches.group_0
                    FROM
                        producer0_field0_matches
                    WHERE 1=1
                    GROUP BY 1, 2;
                """)
            ),
            SQLQueryTestcase(
                test_name="single_file_with_one_group",
                input_path_patterns={
                    "file": r"file(?P<firstgroup>.*)"
                },
                test_fieldname="file",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);",
                ],
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value"},
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        producer0_field0_matches.group_0
                    FROM
                        producer0_field0_matches
                    WHERE 1=1
                    GROUP BY 1, 2;
                """)
            ),

            SQLQueryTestcase(
                test_name="single_file_with_two_groups",
                input_path_patterns={
                    "file": r"file(?P<firstgroup>.*)(?P<secondgroup>.*)"
                },
                test_fieldname="file",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);",
                ],
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0,
                            group_1
                        )
                    VALUES (?, ?, ?)
                """),
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value", "secondgroup": "rndm_group_value2"},
                insert_file_sql_binds=["rndm_filename", "rndm_group_value", "rndm_group_value2"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        producer0_field0_matches.group_0,
                        producer0_field0_matches.group_1
                    FROM
                        producer0_field0_matches
                    WHERE 1=1
                    GROUP BY 1, 2, 3;
                """),
            ),

            # Multifile ################################################################################################
            SQLQueryTestcase(
                test_name="multifile_with_no_groups",
                input_path_patterns={
                    "file1": [r"file1.*"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"__file1": "rndm_group_value"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        GROUP_CONCAT(producer0_field0_matches_mod.filename, ',') AS "field_0",
                        producer0_field0_matches_mod.group_0
                    FROM
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0
                            FROM
                                producer0_field0_matches
                            GROUP BY
                                group_0
                        ) as producer0_field0_matches_mod
                    WHERE
                        1=1
                    GROUP BY 2;
                """),
            ),
            SQLQueryTestcase(
                test_name="multifile_with_one_group",
                input_path_patterns={
                    "file1": [r"file1(?P<firstgroup>.*)"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        GROUP_CONCAT(producer0_field0_matches_mod.filename, ',') AS "field_0",
                        producer0_field0_matches_mod.group_0
                    FROM
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0
                            FROM
                                producer0_field0_matches
                            GROUP BY
                                group_0
                        ) as producer0_field0_matches_mod
                    WHERE
                        1=1
                    GROUP BY 2;
                """),
            ),

            SQLQueryTestcase(
                test_name="multifile_with_two_groups",
                input_path_patterns={
                    "file1": [r"file1(?P<firstgroup>.*)(?P<secondgroup>.*)"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value", "secondgroup": "rndm_group_value2"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0,
                            group_1
                        )
                    VALUES (?, ?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value", "rndm_group_value2"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        GROUP_CONCAT(producer0_field0_matches_mod.filename, ',') AS "field_0",
                        producer0_field0_matches_mod.group_0,
                        producer0_field0_matches_mod.group_1
                    FROM
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0,
                                group_1
                            FROM
                                producer0_field0_matches
                            GROUP BY
                                group_0,
                                group_1
                        ) as producer0_field0_matches_mod
                    WHERE
                        1=1
                    GROUP BY 2, 3;
                """)
            ),

            # Two Singlefiles ##########################################################################################
            SQLQueryTestcase(
                test_name="two_single_files_with_no_groups",
                input_path_patterns={
                    "file1": r"file1",
                    "file2": r"file2",
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);",
                    "CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_1 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"__file1": "rndm_group_value"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        producer0_field1_matches.filename AS "field_1",
                        producer0_field0_matches.group_0,
                        producer0_field1_matches.group_1
                    FROM
                        producer0_field0_matches,
                        producer0_field1_matches
                    WHERE
                        1=1
                    GROUP BY 1, 2, 3, 4;
                """)
            ),

            SQLQueryTestcase(
                test_name="two_single_files_with_one_group",
                input_path_patterns={
                    "file1": r"file1(?P<firstgroup>.*)",
                    "file2": r"file2(?P<firstgroup>.*)",
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);",
                    "CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_0 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        producer0_field1_matches.filename AS "field_1",
                        producer0_field0_matches.group_0
                    FROM
                        producer0_field0_matches,
                        producer0_field1_matches
                    WHERE
                        producer0_field0_matches.group_0 = producer0_field1_matches.group_0
                    GROUP BY 1, 2, 3;
                """)
            ),

            SQLQueryTestcase(
                test_name="two_single_files_with_two_groups",
                input_path_patterns={
                    "file1": r"file1(?P<firstgroup>.*)(?P<secondgroup>.*)",
                    "file2": r"file2(?P<firstgroup>.*)(?P<secondgroup>.*)",
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);",
                    "CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value", "secondgroup": "rndm_group_value2"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0,
                            group_1
                        )
                    VALUES (?, ?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value", "rndm_group_value2"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        producer0_field1_matches.filename AS "field_1",
                        producer0_field0_matches.group_0,
                        producer0_field0_matches.group_1
                    FROM
                        producer0_field0_matches,
                        producer0_field1_matches
                    WHERE
                        producer0_field0_matches.group_0 = producer0_field1_matches.group_0
                        AND producer0_field0_matches.group_1 = producer0_field1_matches.group_1
                    GROUP BY 1, 2, 3, 4;
                """)
            ),

            # Two Multifiles ###########################################################################################
            SQLQueryTestcase(
                test_name="two_multifile_with_no_groups",
                input_path_patterns={
                    "file1": [r"file1.*"],
                    "file2": [r"file2.*"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);",
                    "CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_1 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"__file1": "rndm_group_value"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        GROUP_CONCAT(producer0_field0_matches_mod.filename, ',') AS "field_0",
                        GROUP_CONCAT(producer0_field1_matches_mod.filename, ',') AS "field_1",
                        producer0_field0_matches_mod.group_0,
                        producer0_field1_matches_mod.group_1
                    FROM
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0
                            FROM
                                producer0_field0_matches
                            GROUP BY
                                group_0
                        ) as producer0_field0_matches_mod,
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_1
                            FROM
                                producer0_field1_matches
                            GROUP BY
                                group_1
                        ) as producer0_field1_matches_mod
                    WHERE
                        1=1
                    GROUP BY 3, 4;
                """),
            ),

            SQLQueryTestcase(
                test_name="two_multifile_with_one_group",
                input_path_patterns={
                    "file1": [r"file1(?P<firstgroup>.*)"],
                    "file2": [r"file2(?P<firstgroup>.*)"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);",
                    "CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_0 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        GROUP_CONCAT(producer0_field0_matches_mod.filename, ',') AS "field_0",
                        GROUP_CONCAT(producer0_field1_matches_mod.filename, ',') AS "field_1",
                        producer0_field0_matches_mod.group_0
                    FROM
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0
                            FROM
                                producer0_field0_matches
                            GROUP BY
                                group_0
                        ) as producer0_field0_matches_mod,
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0
                            FROM
                                producer0_field1_matches
                            GROUP BY
                                group_0
                        ) as producer0_field1_matches_mod
                    WHERE
                        producer0_field0_matches_mod.group_0 = producer0_field1_matches_mod.group_0
                    GROUP BY 3;
                """),
            ),

            SQLQueryTestcase(
                test_name="two_multifile_with_two_groups",
                input_path_patterns={
                    "file1": [r"file1(?P<firstgroup>.*)(?P<secondgroup>.*)"],
                    "file2": [r"file2(?P<firstgroup>.*)(?P<secondgroup>.*)"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    "CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);",
                    "CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);",
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "rndm_group_value", "secondgroup": "rndm_group_value2"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0,
                            group_1
                        )
                    VALUES (?, ?, ?)
                """),
                insert_file_sql_binds=["rndm_filename", "rndm_group_value", "rndm_group_value2"],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        GROUP_CONCAT(producer0_field0_matches_mod.filename, ',') AS "field_0",
                        GROUP_CONCAT(producer0_field1_matches_mod.filename, ',') AS "field_1",
                        producer0_field0_matches_mod.group_0,
                        producer0_field0_matches_mod.group_1
                    FROM
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0,
                                group_1
                            FROM
                                producer0_field0_matches
                            GROUP BY
                                group_0,
                                group_1
                        ) as producer0_field0_matches_mod,
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0,
                                group_1
                            FROM
                                producer0_field1_matches
                            GROUP BY
                                group_0,
                                group_1
                        ) as producer0_field1_matches_mod
                    WHERE
                        producer0_field0_matches_mod.group_0 = producer0_field1_matches_mod.group_0
                        AND producer0_field0_matches_mod.group_1 = producer0_field1_matches_mod.group_1
                    GROUP BY 3, 4;
                """)
            ),

            # One Singlefile One Multifile #############################################################################

            SQLQueryTestcase(
                test_name="one_singlefile_one_multifile_with_no_groups",
                input_path_patterns={
                    "file1": r"file1",
                    "file2": [r"file2.*"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    'CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);',
                    'CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_1 TEXT);',
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"__file1": "randomvalue"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=['rndm_filename', 'randomvalue'],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        GROUP_CONCAT(producer0_field1_matches_mod.filename, ',') AS "field_1",
                        producer0_field0_matches.group_0,
                        producer0_field1_matches_mod.group_1
                    FROM
                        producer0_field0_matches,
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_1
                            FROM
                                producer0_field1_matches
                            GROUP BY
                                group_1
                        ) as producer0_field1_matches_mod
                    WHERE
                        1=1
                    GROUP BY
                        1, 3, 4;
                """),
            ),
            SQLQueryTestcase(
                test_name="one_singlefile_one_multifile_with_one_group",
                input_path_patterns={
                    "file1": r"file1(?P<firstgroup>.*)",
                    "file2": [r"file2(?P<firstgroup>.*).*"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    'CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT);',
                    'CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_0 TEXT);',
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "randomvalue"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0
                        )
                    VALUES (?, ?)
                """),
                insert_file_sql_binds=['rndm_filename', 'randomvalue'],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        GROUP_CONCAT(producer0_field1_matches_mod.filename, ',') AS "field_1",
                        producer0_field0_matches.group_0
                    FROM
                        producer0_field0_matches,
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0
                            FROM
                                producer0_field1_matches
                            GROUP BY
                                group_0
                        ) as producer0_field1_matches_mod
                    WHERE
                        producer0_field0_matches.group_0 = producer0_field1_matches_mod.group_0
                    GROUP BY
                        1, 3;
                """),
            ),
            SQLQueryTestcase(
                test_name="one_singlefile_one_multifile_with_two_groups",
                input_path_patterns={
                    "file1": r"file1(?P<firstgroup>.*)(?P<secondgroup>.*)",
                    "file2": [r"file2(?P<firstgroup>.*)(?P<secondgroup>.*).*"],
                },
                test_fieldname="file1",
                init_tables_sql=[
                    'CREATE TABLE producer0_field0_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);',
                    'CREATE TABLE producer0_field1_matches (filename TEXT UNIQUE, group_0 TEXT, group_1 TEXT);',
                ],
                insert_file_filename="rndm_filename",
                insert_file_groups={"firstgroup": "randomvalue", "secondgroup": "anotherrandomvalue"},
                insert_file_sql=reduce_whitespace("""
                    INSERT INTO
                        producer0_field0_matches (
                            filename,
                            group_0,
                            group_1
                        )
                    VALUES (?, ?, ?)
                """),
                insert_file_sql_binds=['rndm_filename', 'randomvalue', 'anotherrandomvalue'],
                query_filesets_sql=reduce_whitespace("""
                    SELECT
                        producer0_field0_matches.filename AS "field_0",
                        GROUP_CONCAT(producer0_field1_matches_mod.filename, ',') AS "field_1",
                        producer0_field0_matches.group_0,
                        producer0_field0_matches.group_1
                    FROM
                        producer0_field0_matches,
                        (
                            SELECT
                                GROUP_CONCAT(REPLACE(REPLACE(filename, '\\', '\\\\'), ',', '\\,'), ',') as filename,
                                group_0,
                                group_1
                            FROM
                                producer0_field1_matches
                            GROUP BY
                                group_0,
                                group_1
                        ) as producer0_field1_matches_mod
                    WHERE
                        producer0_field0_matches.group_0 = producer0_field1_matches_mod.group_0
                        AND producer0_field0_matches.group_1 = producer0_field1_matches_mod.group_1
                    GROUP BY
                        1, 3, 4;
                """),
            ),

        ]

        for case in cases:
            with self.subTest(case.test_name):
                fileset = SqlFileSet([
                    Producer(
                        name="my_producer",
                        input_path_patterns=case.input_path_patterns,
                        function=dummy_function,
                    )
                ])

                # Create database tables
                self.assertListEqual(fileset._init_fileset_database_sql(0), case.init_tables_sql)

                # TODO: I dont know if this should be allowed, empty group matches? Maybe? but if we have a regex match shouldn't we be matching all groups?
                # insert_sql, binds = fileset.insert_new_file_querystring(0, "file", "rndm_filename", {})

                # Insert File into Database SQL
                insert_sql, binds = fileset._insert_file_into_database_sql(0, case.test_fieldname, case.insert_file_filename, case.insert_file_groups)
                self.assertListEqual(binds, case.insert_file_sql_binds)
                self.assertEqual(insert_sql, case.insert_file_sql)

                # Remove File From database SQL
                self.assertEqual(
                    fileset._remove_file_from_database_sql(0, case.test_fieldname),
                    "DELETE FROM producer0_field0_matches WHERE filename = :filename",
                )

                # Query Fileset from database SQL
                self.assertEqual(fileset._query_filesets_from_database_sql(0), case.query_filesets_sql)
