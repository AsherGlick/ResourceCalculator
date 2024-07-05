from typing import Dict, List, Tuple, TypedDict, Protocol, Any, Generic, TypeVar, Callable
import unittest
from unittest.mock import Mock

from .producer import InputFileDatatype, Producer
from .scheduler import Scheduler

from dataclasses import dataclass


@dataclass
class FunctionCall(Generic[InputFileDatatype]):
    input_paths: InputFileDatatype
    groups: Dict[str, str]


class Integration_Tests(unittest.TestCase):
    maxDiff = 999999

    ############################################################################
    # test_single_shared_filer
    #
    # Test that a set of grouped files with a single shared file get converted
    # into Creators properly.
    ############################################################################
    def test_single_group(self) -> None:

        class Input(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "global_config": r"^global_configs?\.txt$",
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[
                producer
            ],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    groups={
                        "title": "one",
                        "__global_config": "global_config.txt",
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_config.txt'
                    },
                    groups={
                        "title": "two",
                        "__global_config": "global_config.txt",
                    }
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

        class Input(TypedDict):
            data_file: str
            partial_files: List[str]

        function_calls: List[FunctionCall[Input]] = []
        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "partial_files": [r"partial_(?P<title>[a-z]+)_[0-9]+\.txt$"],
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[
                producer
            ],
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
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "partial_files": ["partial_one_1.txt", "partial_one_2.txt", "partial_one_3.txt", "partial_one_4.txt"],
                    },
                    groups={
                        "title": "one"
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        "partial_files": ["partial_two_11.txt", "partial_two_12.txt", "partial_two_13.txt", "partial_two_14.txt"],
                    },
                    groups={
                        "title": "two"
                    }
                )
            ]
        )

    ############################################################################
    # test_empty_field_string
    #
    # Tests that the ability to add an empty string as a field pattern works.
    # TODO: We now that we no longer have the `paths` step we should issue a
    #   warning when this happens because at best it is equivalent to not having
    #   a field, at worst it is equivalent to preventing the producer from ever
    #   being run because "" is never going to be a file.
    ############################################################################
    def test_empty_field_string(self) -> None:
        class Input(TypedDict):
            data_file: str
            value_file: str
            source_file: str

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            input_files["source_file"] += "_extention_on_blank"
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Text Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "source_file": "",
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[
                producer
            ],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
            ]
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "source_file": "_extention_on_blank",
                    },
                    groups={
                        "title": "one",
                    }
                ),
                FunctionCall(
                    input_paths={
                        "data_file": "data_two.txt",
                        "value_file": "value_two.txt",
                        "source_file": "_extention_on_blank",
                    },
                    groups={
                        "title": "two"
                    }
                )
            ]
        )

    ############################################################################
    # test_empty_field_array
    #
    # Tests that the ability to add an empty array as a field pattern works.
    # TODO: We now that we no longer have the `paths` step we should issue a
    #   warning when this happens because at best it is equivalent to not having
    #   a field, at worst it is equivalent to preventing the producer from ever
    #   being run because "" is never going to be a file.    
    ############################################################################
    def test_empty_field_array(self) -> None:
        class Input(TypedDict):
            data_file: str
            value_file: str
            source_files: List[str]

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            input_files["source_files"].append("extention")
            input_files["source_files"].append("on")
            input_files["source_files"].append("blank")
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "source_files": [],
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "source_files": ["extention", "on", "blank"],
                    },
                    groups={
                        "title": "one"
                    }
                ),
                FunctionCall(
                    input_paths={
                        "data_file": "data_two.txt",
                        "value_file": "value_two.txt",
                        "source_files": ["extention", "on", "blank"],
                    },
                    groups={
                        "title": "two"
                    }

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

        class Input(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return["output_" + groups["title"] + "_" + input_files["global_config"]]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "global_config": r"^global_configs?\.txt$",
            },
            function=function,
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
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    groups={
                        "title": "one",
                        "__global_config": "global_config.txt"
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_config.txt'
                    },
                    groups={
                        "title": "two",
                        "__global_config": "global_config.txt"
                    }
                ),
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_configs.txt",
                    },
                    groups={
                        "title": "one",
                        "__global_config": "global_configs.txt"
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_configs.txt'
                    },
                    groups={
                        "title": "two",
                        "__global_config": "global_configs.txt"
                    }
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

        class Input(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + "_" + groups["language"] + ".txt" ]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)_(?P<language>[a-z]+)\.txt$",
                "global_config": r"^global_config_(?P<language>[a-z]+)\.txt$",
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[
                producer
            ],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one_german.txt',
                'value_one_spanish.txt',
                'value_two_german.txt',
                'value_two_spanish.txt',
                'global_config_german.txt',
                'global_config_spanish.txt',
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one_german.txt",
                        "global_config": "global_config_german.txt",
                    },
                    groups={
                        "title": "one",
                        "language": "german",
                    }
                ),
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one_spanish.txt",
                        "global_config": "global_config_spanish.txt",
                    },
                    groups={
                        "title": "one",
                        "language": "spanish",
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two_german.txt',
                        'global_config': 'global_config_german.txt'
                    },
                    groups={
                        "title": "two",
                        "language": "german",
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two_spanish.txt',
                        'global_config': 'global_config_spanish.txt'
                    },
                    groups={
                        "title": "two",
                        "language": "spanish",
                    }
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
        class Input(TypedDict):
            data_file: str
            partial_files: List[str]

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "partial_files": [r"partial\\?,?_(?P<title>[a-z]+)_[0-9]+\.txt$"],
            },
            function=function,
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
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "partial_files": [
                            "partial,_one_4.txt",
                            "partial\\_one_2.txt",
                            "partial_one_1.txt",
                            "partial_one_3.txt"
                        ],
                    },
                    groups={
                        "title": "one"
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        "partial_files": [
                            "partial,_two_14.txt",
                            "partial\\_two_12.txt",
                            "partial_two_11.txt",
                            "partial_two_13.txt"
                        ],
                    },
                    groups={
                        "title": "two"
                    }
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

        class Input(TypedDict):
            data_file: str

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + input_files["data_file"]]

        producer: Producer[Input] = Producer(
            name="Test Case2",
            input_path_patterns={
                "data_file": r"^data_[a-z]+\.txt$",
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                    },
                    groups={
                        "__data_file": "data_one.txt",
                    }
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                    },
                    groups={
                        "__data_file": "data_two.txt",
                    }
                )
            ]
        )

    ############################################################################
    # test_array_no_match_group
    #
    # Test that an array regex without a match group is properly combined to be
    # a single action instead of being split up to multiple actions
    ############################################################################
    def test_array_no_match_group(self) -> None:
        class Input(TypedDict):
            data_file: List[str]

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_file.txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": [r"^data_[a-z]+\.txt$"],
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": [
                            "data_one.txt",
                            "data_two.txt"
                        ],
                    },
                    groups={
                        "__data_file": "",
                    }
                ),
            ]
        )

    ############################################################################
    # test_double_array_no_match_group
    #
    # Tests that having two arrays of data in the same producer correctly
    # produces the desired output when the arrays do not have any match groups.
    ############################################################################
    def test_double_array_no_match_group(self) -> None:

        class Input(TypedDict):
            data_file: List[str]
            value_file: List[str]

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_file.txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": [r"^data_[a-z]+\.txt$"],
                "value_file": [r"^value_[a-z]+\.txt$"],
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt'
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
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
                    groups={
                        "__data_file": "",
                        "__value_file": "",
                    }
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

        class Input(TypedDict):
            data_file: List[str]
            value_file: List[str]

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": [r"^data_(?P<title>[a-z]+)_[0-9]\.txt$"],
                "value_file": [r"^value_(?P<title>[a-z]+)_[0-9]\.txt$"],
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one_1.txt',
                'data_one_2.txt',
                'data_two_1.txt',
                'data_two_2.txt',
                'value_one_1.txt',
                'value_one_2.txt',
                'value_two_1.txt',
                'value_two_2.txt'
            ],
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
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
                    groups={
                        "title": "one",
                    },
                ),
                FunctionCall(
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
                    groups={
                        "title": "two",
                    },
                )
            ]
        )

    ############################################################################
    # test_file_addition_to_existing_files
    #
    # Tests that we will generate new actions based on existing files if a new
    # file is added that would complete a proucer regex combination.
    ############################################################################
    def test_file_addition_to_existing_files(self) -> None:
        class Input(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "global_config": r"^global_configs?\.txt$",
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[
                'data_one.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ]
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    groups={
                        "title": "one",
                        "__global_config": "global_config.txt",
                    }
                ),
            ]
        )

        # Reset function_calls so we only see the function calls that are made
        # as a result of calling add_or_update_files() with the new file.
        function_calls = []

        scheduler.add_or_update_files(
            [
                'data_two.txt'
            ]
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_config.txt'
                    },
                    groups={
                        "title": "two",
                        "__global_config": "global_config.txt",
                    }
                )
            ]
        )

    ############################################################################
    # test_file_readdition
    #
    # Test that when a file is re-added it triggers all of the actions it is
    # supposed to and none of the actions it is not supposed to.
    ############################################################################
    def test_file_readdition(self) -> None:
        class Input(TypedDict):
            data_file: str
            value_file: str
            global_config: str

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_file": r"value_(?P<title>[a-z]+)\.txt$",
                "global_config": r"^global_configs?\.txt$",
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[
                producer
            ],
            initial_filepaths=[
                'data_one.txt',
                'data_two.txt',
                'value_one.txt',
                'value_two.txt',
                'global_config.txt',
            ]
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    groups={
                        "title": "one",
                        "__global_config": "global_config.txt"
                    },
                ),
                FunctionCall(
                    input_paths={
                        'data_file': 'data_two.txt',
                        'value_file': 'value_two.txt',
                        'global_config': 'global_config.txt'
                    },
                    groups={
                        "title": "two",
                        "__global_config": "global_config.txt"
                    },
                )
            ]
        )


        # Reset function_calls so we only see the function calls that are made
        # as a result of calling add_or_update_files() with the new file.
        function_calls = []


        scheduler.add_or_update_files(
            [
                'data_one.txt',
            ]
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_file": "value_one.txt",
                        "global_config": "global_config.txt",
                    },
                    groups={
                        "title": "one",
                        "__global_config": "global_config.txt"
                    },
                ),
            ]
        )

#     def test_file_deletion(self) -> None:
#         class InputFileDatatype(TypedDict):
#             data_file: str
#             value_file: str
#             global_config: str

#         class OutputFileDatatype(TypedDict):
#             data_file: str

#         def paths(input_files: InputFileDatatype, groups: Dict[str, str]) -> Tuple[InputFileDatatype, OutputFileDatatype]:
#             return (input_files, {"data_file": "output_" + groups["title"] + ".txt"})

#         def function(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
#             return None  # pragma: no cover

#         producer: Producer[InputFileDatatype, OutputFileDatatype] = Producer(
#             input_path_patterns={
#                 "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
#                 "value_file": r"value_(?P<title>[a-z]+)\.txt$",
#                 "global_config": r"^global_configs?\.txt$",
#             },
#             paths=paths,
#             function=function,
#             categories=["test"],
#         )

#         scheduler = Scheduler(
#             producer_list=[producer],
#             initial_filepaths=[],
#         )
#         scheduler.build_new_creators(
#             [
#                 'data_one.txt',
#                 'data_two.txt',
#                 'value_one.txt',
#                 'value_two.txt',
#                 'global_config.txt',
#             ]
#         )
#         scheduler.delete_files(
#             [
#                 'data_two.txt',
#                 'value_two.txt',
#             ]
#         )

#         # Force a rebuild of the creators to be sure that deleting the files
#         # did not just delete the creators from the list and leave the files
#         scheduler.build_new_creators(
#             [
#             'global_config.txt'
#             ]
#         )

#         self.assertCountEqual(
#             scheduler.creator_list.values(),
#             [
#                 Creator(
#                     input_paths={
#                         "data_file": "data_one.txt",
#                         "value_file": "value_one.txt",
#                         "global_config": "global_config.txt",
#                     },
#                     output_paths={
#                         "data_file": "output_one.txt"
#                     },
#                     function=function,
#                     categories=["test"]
#                 ),
#             ]
#         )
    
    def test_new_file_in_array(self) -> None:
        class Input(TypedDict):
            data_file: str
            value_files: List[str]

        function_calls: List[FunctionCall[Input]] = []

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]

        producer: Producer[Input] = Producer(
            name="Test Case",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
                "value_files": [r"value_(?P<title>[a-z]+).*\.txt$"],
            },
            function=function,
        )

        scheduler = Scheduler(
            producer_list=[producer],
            initial_filepaths=[],
        )
        scheduler.add_or_update_files(
            [
                'data_one.txt',
                'value_one_1.txt',
                'value_one_2.txt',
            ]
        )


        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_files": ["value_one_1.txt", "value_one_2.txt"],
                    },
                    groups={
                        "title": "one",
                    }
                ),
            ]
        )

        # Reset function_calls so we only see the function calls that are made
        # as a result of calling add_or_update_files() with the new file.
        function_calls = []

        scheduler.add_or_update_files(
            [
                'value_one_3.txt',
            ]
        )

        self.assertCountEqual(
            function_calls,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                        "value_files": ["value_one_1.txt", "value_one_2.txt", "value_one_3.txt"],
                    },
                    groups={
                        "title": "one",
                    }
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
    # # TODO:
    # # This should probably throw an error of some sort stating that it found
    # # multiple different possibilities for a group. I dont think we actually
    # # want two different action to be run here becuase the user should either
    # # be using an additional group to indicate the difference in files, or
    # # should be using an array.
    # ############################################################################
    # def test_mutliple_options_with_group(self) -> None:

    #     class Input(TypedDict):
    #         data_file: str

    #     function_calls: List[FunctionCall[Input]] = []

    #     def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
    #         function_calls.append(FunctionCall(input_files, groups))
    #         return ["output_" + input_files["data_file"]]

    #     producer: Producer[Input] = Producer(
    #         name="Test Case",
    #         input_path_patterns={
    #             "data_file": r"^data_(?P<title>[a-z]+)_.\.txt$",
    #         },
    #         function=function,
    #     )

    #     scheduler = Scheduler(
    #         producer_list=[producer],
    #         initial_filepaths=[],
    #     )
    #     scheduler.add_or_update_files(
    #         files=[
    #             'data_one_1.txt',
    #             'data_one_2.txt',
    #         ]
    #     )

    #     self.assertCountEqual(
    #         function_calls,
    #         [
    #             FunctionCall(
    #                 input_paths={
    #                     "data_file": "data_one_1.txt",
    #                 },
    #                 groups={
    #                     "title": "one",
    #                 }
    #             ),
    #             FunctionCall(
    #                 input_paths={
    #                     'data_file': 'data_one_2.txt',
    #                 },
    #                 groups={
    #                     "title": "one",
    #                 }
    #             )
    #         ]
    #     )


    ############################################################################
    # test_cascading_actions
    #
    # Test that when one producer creates files that are consumed by another
    # producer, the second producer successfully processes those files.
    ############################################################################
    def test_cascading_actions(self) -> None:

        class Input(TypedDict):
            data_file: str

        function_calls_data: List[FunctionCall[Input]] = []

        def function_data(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls_data.append(FunctionCall(input_files, groups))
            return ["value_" + groups["title"] + ".txt"]

        function_calls_value: List[FunctionCall[Input]] = []

        def function_value(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls_value.append(FunctionCall(input_files, groups))
            return ["output_" + groups["title"] + ".txt"]


        producer_data: Producer[Input] = Producer(
            name="Test Case - Data",
            input_path_patterns={
                "data_file": r"^data_(?P<title>[a-z]+)\.txt$",
            },
            function=function_data,
        )
        producer_value: Producer[Input] = Producer(
            name="Test Case - Value",
            input_path_patterns={
                "data_file": r"^value_(?P<title>[a-z]+)\.txt$",
            },
            function=function_value,
        )


        scheduler = Scheduler(
            producer_list=[
                producer_data,
                producer_value,
            ],
            initial_filepaths=[
                'data_one.txt',
            ],
        )

        self.assertCountEqual(
            function_calls_data,
            [
                FunctionCall(
                    input_paths={
                        "data_file": "data_one.txt",
                    },
                    groups={
                        "title": "one",
                    }
                ),
            ]
        )
        self.assertCountEqual(
            function_calls_value,
            [
                FunctionCall(
                    input_paths={
                        'data_file': 'value_one.txt',
                    },
                    groups={
                        "title": "one",
                    }
                )
            ]
        )


    ############################################################################
    ############################################################################
    def test_inline_update_of_array(self) -> None:

        class Input(TypedDict):
            data_list: List[str]

        function_calls_init: List[FunctionCall[Input]] = []
        def function_init(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls_init.append(FunctionCall(input_files, groups))
            return ["array_element_9.txt"]

        function_calls_process: List[FunctionCall[Input]] = []
        def function_process(input_files: Input, groups: Dict[str, str]) -> List[str]:
            function_calls_process.append(FunctionCall(input_files, groups))
            return ["output.txt"]


        producer_data: Producer[Input] = Producer(
            name="Test Case - Init",
            input_path_patterns={
                "data_list": [r"^data_file\.txt$"],
            },
            function=function_init,
        )
        producer_value: Producer[Input] = Producer(
            name="Test Case - Value",
            input_path_patterns={
                "data_list": [r"^array_element_[0-9]\.txt$"]
            },
            function=function_process,
        )


        scheduler = Scheduler(
            producer_list=[
                producer_data,
                producer_value,
            ],
            initial_filepaths=[
                'data_file.txt', # Triggering Function
                'array_element_1.txt',
                'array_element_2.txt',
                'array_element_3.txt',
            ],
        )

        self.assertCountEqual(
            function_calls_init,
            [
                FunctionCall(
                    input_paths={
                        "data_list": ["data_file.txt"],
                    },
                    groups={
                        "__data_list": "",
                    }
                ),
            ]
        )
        self.assertCountEqual(
            function_calls_process,
            [
                FunctionCall(
                    input_paths={
                        'data_list': [
                            'array_element_1.txt',
                            'array_element_2.txt',
                            'array_element_3.txt',
                            'array_element_9.txt',
                        ],
                    },
                    groups={
                        "__data_list": "",
                    }
                )
            ]
        )


    # TODO: Write a test that shows that an action can only replace itself in the unique heap, even if it shares a producer with another action.

class ConfigurationTests(unittest.TestCase):
    maxDiff = 999999

    ############################################################################
    # test_non_unique_producer_name_error
    #
    # The names of producers need to be unique so they can be referenced in
    # subsequent runs.
    ############################################################################
    def test_non_unique_producer_name_error(self):

        class Input(TypedDict):
            data: str

        def function(input_files: Input, groups: Dict[str, str]) -> List[str]:
            return [input_files["data"] + "_output.txt"]

        producer_data: Producer[Input] = Producer(
            name="Test Name",
            input_path_patterns={
                "data": r"^data_file1\.txt$",
            },
            function=function,
        )
        producer_value: Producer[Input] = Producer(
            name="Test Name",
            input_path_patterns={
                "data": r"^data_file2\.txt$"
            },
            function=function,
        )

        with self.assertRaises(ValueError):
            scheduler = Scheduler(
                producer_list=[
                    producer_data,
                    producer_value,
                ],
                initial_filepaths=[
                    'data_file1.txt',
                    'data_file2.txt',
                ],
            )

# class Initialization_Query_Tests(unittest.TestCase):
#     pass

# class Insert_Query_Tests(unittest.TestCase):
#     pass

# class Remove_Query_Tests(unittest.TestCase):
#     pass

# class Filesets_Query_Tests(unittest.TestCase):
#     pass
