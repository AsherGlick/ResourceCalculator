from typing import Dict, List, Tuple, TypedDict
import unittest

from .creator import Creator
from .producer import Producer
from .scheduler import Scheduler


class Test_Basic_Creator_Generation(unittest.TestCase):
    maxDiff = 999999

    ############################################################################
    # test_single_shared_file
    #
    # Test that a set of grouped files with a single shared file get converted
    # into Creators properly.
    ############################################################################
    def test_single_group(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            global_config: str
        class OutputFileDatatype(TypedDict):
            data_file: str


        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return

        producer = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "global_config": r"^global_configs?\.txt$",
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ]
        )

        self.assertListEqual(
            sorted(scheduler.creator_list.values()),
            sorted([
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_config.txt'
                    },
                    output_paths={
                        'data_file': 'output_two.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ])
        )


    ############################################################################
    # test_array_search
    #
    # Test that an array value can be automatically populated by the scheduler.
    # An array value is defined in the input data type and will be filled with
    # all possible regex matches with the same restriction that only files that
    # share all named group values will be present.
    ############################################################################
    def test_array_search(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: str
            partial_files: List[str]

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return


        producer = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "partial_files": [r"partial_(?P<title>[a-z]+)_[0-9]+\.txt$"],
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'partial_one_1.txt',
                'partial_one_2.txt',
                'partial_one_3.txt',
                'partial_one_4.txt',
                'partial_two_11.txt',
                'partial_two_12.txt',
                'partial_two_13.txt',
                'partial_two_14.txt',
            ]
        )

        self.assertListEqual(
            sorted(scheduler.creator_list.values()),
            sorted([
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "partial_files": ["partial_one_1.txt", "partial_one_2.txt", "partial_one_3.txt", "partial_one_4.txt"],
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                        "partial_files": ["partial_two_11.txt", "partial_two_12.txt", "partial_two_13.txt", "partial_two_14.txt"],
                    },
                    output_paths={
                        'data_file': 'output_two.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ])
        )



    # # This still does not work right but that is mostly due to how I am doing
    # # joins in the sqlite table. I will figure out a better way to handle this
    # # test case after the entire system is working with the assumption that
    # # all files exist. The only downside to the current system is that you will
    # # not get an error if a file does not exist, the files corrisponding to it
    # # will just not be processed.
    # def test_missing_fields(self) -> None:

    #     class InputFileDatatype(TypedDict):
    #         data_file: str
    #         data_file_two: str
    #         partial_files: List[str]

    #     class OutputFileDatatype(TypedDict):
    #         data_file: str

    #     def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
    #         return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

    #     def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
    #         return


    #     producer = Producer(
    #         input_path_patterns={
    #             "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
    #             "data_file_two": r"^2data_(?P<title>[a-z]+)\.txt$",
    #             "partial_files": [r"partial_(?P<title>[a-z]+)_[0-9]+\.txt$"],
    #         },
    #         paths=paths,
    #         function=function,
    #         categories=["test"],
    #     )

    #     scheduler = Scheduler(
    #         producer_list=[producer],
    #         initial_filepaths=[
    #             'data_one.txt',
    #             '2data_one.txt',
    #             'partial_one_1.txt',
    #             'partial_one_2.txt',

    #             'data_two.txt',
    #             'partial_two_1.txt',
    #             'partial_two_2.txt',

    #             'data_three.txt',
    #             '2data_three.txt',
    #         ]
    #     )

    #     self.assertListEqual(
    #         sorted(scheduler.creator_list.values()),
    #         sorted([
    #             Creator(
    #                 input_paths={
    #                     "data_file": "data_one.txt",
    #                     "partial_files": ["partial_one_1.txt", "partial_one_2.txt", "partial_one_3.txt", "partial_one_4.txt"],
    #                 },
    #                 output_paths={
    #                     "data_file": "output_one.txt"
    #                 },
    #                 function=function,
    #                 categories=["test"]
    #             ),
    #             Creator(
    #                 input_paths={
    #                     'data_file': 'data_two.txt',
    #                     "partial_files": ["partial_two_11.txt", "partial_two_12.txt", "partial_two_13.txt", "partial_two_14.txt"],
    #                 },
    #                 output_paths={
    #                     'data_file': 'output_two.txt'
    #                 },
    #                 function=function,
    #                 categories=['test']
    #             )
    #         ])
    #     )


    ############################################################################
    # test_empty_field_string
    #
    # Tests that the ability to add an empty string as a field pattern works.
    # An empty string should represent a field that is present but will not be
    # automatically filled by the scheduler and instead is a placeholder for
    # a value set to it inside of the paths() function.
    ############################################################################
    def test_empty_field_string(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            source_file: str
        class OutputFileDatatype(TypedDict):
            data_file: str


        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            input_files["source_file"] += "_extention_on_blank"
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return

        producer = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "source_file": "",
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
            ]
        )

        self.assertListEqual(
            sorted(scheduler.creator_list.values()),
            sorted([
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "source_file": "_extention_on_blank",
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        "data_file": "data_two.txt",
                        "value_file": "value_two.txt",
                        "source_file": "_extention_on_blank",
                    },
                    output_paths={
                        'data_file': 'output_two.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ])
        )


    ############################################################################
    # test_empty_field_array
    #
    # Tests that the ability to add an empty array as a field pattern works.
    # An empty array should represent a field that is present but will not be
    # automatically filled by the scheduler and instead is a placeholder for
    # values set to it inside of the paths() function.
    ############################################################################
    def test_empty_field_array(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            source_files: List[str]
        class OutputFileDatatype(TypedDict):
            data_file: str


        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            input_files["source_files"].append("extention")
            input_files["source_files"].append("on")
            input_files["source_files"].append("blank")

            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return

        producer = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "source_files": [],
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
            ]
        )

        self.assertListEqual(
            sorted(scheduler.creator_list.values()),
            sorted([
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "source_files": ["extention","on","blank"],
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        "data_file": "data_two.txt",
                        "value_file": "value_two.txt",
                        "source_files": ["extention", "on", "blank"],
                    },
                    output_paths={
                        'data_file': 'output_two.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ])
        )

    ############################################################################
    # test_multi_global_file
    #
    # Test to make sure that if there are multiple possible matches for a field
    # then a group is created for each possible combination. In this case there
    # are two static files that each could produce something.
    ############################################################################
    def test_multi_global_file(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            global_config: str
        class OutputFileDatatype(TypedDict):
            data_file: str


        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return

        producer = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "global_config": r"^global_configs?\.txt$",
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
                'global_configs.txt',
            ]
        )

        self.assertListEqual(
            sorted(scheduler.creator_list.values()),
            sorted([
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_config.txt'
                    },
                    output_paths={
                        'data_file': 'output_two.txt'
                    },
                    function=function,
                    categories=['test']
                ),
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_configs.txt",
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_configs.txt'
                    },
                    output_paths={
                        'data_file': 'output_two.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ])
        )

    ############################################################################
    # test_multiple_match_groups
    #
    # Test that if there are multiple regex match groups then we correctly
    # join across them to build input data types.
    ############################################################################
    def test_mutliple_match_groups(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            global_config: str
        class OutputFileDatatype(TypedDict):
            data_file: str


        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + "_" + groups["language"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return

        producer = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)_(?P<language>[a-z]+)\.txt$",
                "global_config": r"^global_config_(?P<language>[a-z]+)\.txt$",
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one_german.txt',
                'value_one_spanish.txt',
                'value_two_german.txt',
                'value_two_spanish.txt',
                'global_config_german.txt',
                'global_config_spanish.txt',
            ]
        )

        self.assertListEqual(
            sorted(scheduler.creator_list.values()),
            sorted([
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one_german.txt",
                        "global_config": "global_config_german.txt",
                    },
                    output_paths={
                        "data_file": "output_one_german.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one_spanish.txt",
                        "global_config": "global_config_spanish.txt",
                    },
                    output_paths={
                        "data_file": "output_one_spanish.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two_german.txt',
                        'global_config': 'global_config_german.txt'
                    },
                    output_paths={
                        'data_file': 'output_two_german.txt'
                    },
                    function=function,
                    categories=['test']
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two_spanish.txt',
                        'global_config': 'global_config_spanish.txt'
                    },
                    output_paths={
                        'data_file': 'output_two_spanish.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ])
        )

    ############################################################################
    # test_filename_with_comma
    #
    # An implementation detail test. Arrays are queried as strings using the
    # SQLite `GROUP_CONCAT` functionality. The delimiter is a `,` comma. This
    # means that all of the existing commas in the filenames are escaped with
    # a `\` backslash. Additionally all backslashes are escaped with a
    # backslash. This is then parsed out into proper arrays without escaped
    # values. This test confirms that some values that we expected to have been
    # escaped at one point in the process are correctly apearing as their
    # unescaped and properly split values. In the future it is possible that
    # this test might be unessasary, however it should not break even if the
    # implementation is swapped out.
    ############################################################################
    def test_filename_with_comma(self) -> None:
        class InputFileDatatype(TypedDict):
            data_file: str
            partial_files: List[str]

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return


        producer = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "partial_files": [r"partial\\?,?_(?P<title>[a-z]+)_[0-9]+\.txt$"],
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'partial_one_1.txt',
                'partial\\_one_2.txt',
                'partial_one_3.txt',
                'partial,_one_4.txt',
                'partial_two_11.txt',
                'partial\\_two_12.txt',
                'partial_two_13.txt',
                'partial,_two_14.txt',
            ]
        )

        self.assertListEqual(
            sorted(scheduler.creator_list.values()),
            sorted([
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "partial_files": ["partial,_one_4.txt", "partial\\_one_2.txt", "partial_one_1.txt", "partial_one_3.txt"],
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                        "partial_files": ["partial,_two_14.txt", "partial\\_two_12.txt", "partial_two_11.txt", "partial_two_13.txt"],
                    },
                    output_paths={
                        'data_file': 'output_two.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ])
        )
