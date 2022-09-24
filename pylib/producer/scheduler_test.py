from typing import Dict, List, Tuple, TypedDict
import unittest

from .creator import Creator
from .producer import Producer
from .scheduler import Scheduler


# TODO: dont use scheduler.build_new_creators() instead just create the files
# that are being tested and use those. This depends on Scheduler being able
# to support working directory inputs instead of using the current working
# directory as the base dir.

class Integration_Tests(unittest.TestCase):
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
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            files=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
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
            return  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
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

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
        )

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
            return  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
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
            return  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "source_files": ["extention", "on", "blank"],
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
            ]
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
            return (input_files, {"data_file": "output_" + groups["title"] + "_" + input_files["global_config"]})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
                'global_configs.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    output_paths={
                        "data_file": "output_one_global_config.txt"
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
                        'data_file': 'output_two_global_config.txt'
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
                        "data_file": "output_one_global_configs.txt"
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
                        'data_file': 'output_two_global_configs.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ]
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
            return  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
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

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
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
    # escaped at one point in the process are correctly appearing as their
    # unescaped and properly split values. In the future it is possible that
    # this test might be unnecessary, however it should not break even if the
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
            return  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
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

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
        )

    ############################################################################
    # test_no_match_group
    #
    # Tests that a producer that has no match group gets converted into
    # Creators successfully
    ############################################################################
    def test_no_match_group(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: str

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + input_files["data_file"]})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
            input_path_patterns={
                "data_file": r"^data_[a-z]+\.txt$",
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'data_two.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                    },
                    output_paths={
                        "data_file": "output_data_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
                Creator(
                    input_paths={
                        'data_file': 'data_two.txt',
                    },
                    output_paths={
                        'data_file': 'output_data_two.txt'
                    },
                    function=function,
                    categories=['test']
                )
            ]
        )

    ############################################################################
    # test_double_array_no_match_group
    #
    # Tests that having two arrays of data in the same producer correctly
    # produces the desired output when the arrays do not have any match groups.
    ############################################################################
    def test_double_array_no_match_group(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: List[str]
            value_file: List[str]

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_file.txt"})


        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
            input_path_patterns={
                "data_file": [r"^data_[a-z]+\.txt$"],
                "value_file": [r"^value_[a-z]+\.txt"],
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt'
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
                Creator(
                    input_paths={
                        "data_file": [
                            "data_one.txt",
                            "data_two.txt"
                        ],
                        "value_file": [
                            "value_one.txt",
                            "value_two.txt"
                        ]
                    },
                    output_paths={
                        "data_file": "output_file.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
            ]
        )

    ############################################################################
    # test_double_array
    #
    # Tests that having two arrays of data in the same producer correctly
    # produces the desired output.
    ############################################################################
    def test_double_array(self) -> None:

        class InputFileDatatype(TypedDict):
            data_file: List[str]
            value_file: List[str]

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
            input_path_patterns={
                "data_file": [r"^data_(?P<title>[a-z]+)_[0-9]\.txt$"],
                "value_file": [r"^value_(?P<title>[a-z]+)_[0-9]\.txt$"],
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one_1.txt',
                'data_one_2.txt',
                'data_two_1.txt',
                'data_two_2.txt',
                'value_one_1.txt',
                'value_one_2.txt',
                'value_two_1.txt',
                'value_two_2.txt'
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
                Creator(
                    input_paths={
                        'data_file': [
                            'data_one_1.txt',
                            'data_one_2.txt',
                        ],
                        'value_file': [
                            'value_one_1.txt',
                            'value_one_2.txt',
                        ]
                    },
                    output_paths={'data_file': 'output_one.txt'},
                    function=function,
                    categories=['test']
                ),
                Creator(
                    input_paths={
                        'data_file': [
                            'data_two_1.txt',
                            'data_two_2.txt',
                        ],
                        'value_file': [
                            'value_two_1.txt',
                            'value_two_2.txt',
                        ]
                    },
                    output_paths={'data_file': 'output_two.txt'},
                    function=function,
                    categories=['test']
                )
            ]
        )

    def test_file_addition_to_existing_set(self) -> None:
        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
        )

        scheduler.build_new_creators(
            [
                'data_two.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
        )


    def test_double_file_addition(self) -> None:
        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ]
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
        )


    def test_file_deletion(self) -> None:
        class InputFileDatatype(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
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
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ]
        )
        scheduler.delete_files(
            [
                'data_two.txt',
                'value_two.txt',
            ]
        )

        # Force a rebuild of the creators to be sure that deleting the files
        # did not just delete the creators from the list and leave the files
        scheduler.build_new_creators(
            [
            'global_config.txt'
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
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
            ]
        )

    def test_new_file_in_group(self) -> None:
        class InputFileDatatype(TypedDict):
            data_file: str
            value_files: List[str]

        class OutputFileDatatype(TypedDict):
            data_file: str

        def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
            return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

        def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
            return None  # pragma: no cover

        producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_files": [r"value_(?P<title>[a-z]+).*\.txt$"],
            },
            paths=paths,
            function=function,
            categories=["test"],
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[],
        )
        scheduler.build_new_creators(
            [
                'data_one.txt',
                'value_one_1.txt',
                'value_one_2.txt',
            ]
        )

        scheduler.build_new_creators(
            [
                'value_one_3.txt',
            ]
        )

        self.assertCountEqual(
            scheduler.creator_list.values(),
            [
                Creator(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_files": ["value_one_1.txt", "value_one_2.txt", "value_one_3.txt"],
                    },
                    output_paths={
                        "data_file": "output_one.txt"
                    },
                    function=function,
                    categories=["test"]
                ),
            ]
        )

    # TODO: Add a test like test_new_file_in_group but where regex for the new
    # file does not have a regex group in it

    # TODO: Add a test where there is an array of files that dont have a group
    # and they have to be placed into at least two different filesets


    # ############################################################################
    # # test_mutliple_options_with_group
    # #
    # # Test that a set of grouped files with a single shared file get converted
    # # into Creators properly.
    # ############################################################################
    # def test_single_group(self) -> None:

    #     class InputFileDatatype(TypedDict):
    #         data_file: str

    #     class OutputFileDatatype(TypedDict):
    #         data_file: str

    #     def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
    #         return (input_files, {"data_file": "output_" + input_files["data_file"]})

    #     def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
    #         return None  # pragma: no cover

    #     producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
    #         input_path_patterns={
    #             "data_file": r"^data_(?P<title>[a-z]+)_.\.txt$",
    #         },
    #         paths=paths,
    #         function=function,
    #         categories=["test"],
    #     )

    #     scheduler = Scheduler(
    #         producer_list=[producer],
    #         initial_filepaths=[],
    #     )
    #     scheduler.build_new_creators(
    #         files=[
    #             'data_one_1.txt',
    #             'data_one_2.txt',
    #         ]
    #     )

    #     self.assertCountEqual(
    #         scheduler.creator_list.values(),
    #         [
    #             Creator(
    #                 input_paths={
    #                     "data_file": "data_one_1.txt",
    #                 },
    #                 output_paths={
    #                     "data_file": "output_data_one_1.txt"
    #                 },
    #                 function=function,
    #                 categories=["test"]
    #             ),
    #             Creator(
    #                 input_paths={
    #                     'data_file': 'data_one_2.txt',
    #                 },
    #                 output_paths={
    #                     'data_file': 'output_data_one_2.txt'
    #                 },
    #                 function=function,
    #                 categories=['test']
    #             )
    #         ]
    #     )


class Initialization_Query_Tests(unittest.TestCase):
    pass

class Insert_Query_Tests(unittest.TestCase):
    pass

class Remove_Query_Tests(unittest.TestCase):
    pass

class Filesets_Query_Tests(unittest.TestCase):
    pass
