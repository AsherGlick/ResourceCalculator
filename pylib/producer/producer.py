from dataclasses import dataclass
from typing import List, Callable, Any, Union, Set, Tuple, TypeVar, Generic, Dict, TypedDict, Iterable, Final
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

    # A list of file regex matches. If a file is changed that matches one of
    # these regex matches then this producer will trigger.
    _input_path_patterns: InputFileDatatype

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
        self._field_to_field_id: Dict[str, int] = {}
        field_name: str
        for field_index, field_name in enumerate(input_path_patterns):
            self._field_to_field_id[field_name] = field_index

        # A map between each unique group in the field and a unique integer that
        # is guarenteed to be a safe sql name.
        self._regex_group_to_index: Dict[str, int] = {}
        all_regex_groups: Set[str] = set()

        # Preprocess all the regex data
        # mypy yells at using .items() on a typed dict even though it is a dict
        for field_name, field_pattern in input_path_patterns.items():  # type:ignore


            field_regex: re.Pattern[str] 
            # regex_string: str
            if isinstance(field_pattern, str):
                if field_pattern == "":
                    continue

                field_regex: re.Pattern[str] = re.compile(field_pattern)
                if len(field_regex.groupindex) == 0:
                    field_regex = re.compile("(?P<{group_name}>{original_regex})".format(
                        group_name="__" + field_name,
                        original_regex=field_pattern,
                    ))




            elif isinstance(field_pattern, list):
                if len(field_pattern) == 0:
                    continue
                if len(field_pattern) > 1:
                    raise TypeError

                # If there is no regex group in this array sequence then set
                # a group that matches an empty string. We dont want to match
                # the full string like we did for the single element field
                # becuase that will cause each element of the array to be split
                # up into different groups.
                field_regex: re.Pattern[str] = re.compile(field_pattern[0])
                if len(field_regex.groupindex) == 0:
                    field_regex = re.compile("(?P<{group_name}>){original_regex}".format(
                        group_name="__" + field_name,
                        original_regex=field_pattern[0],
                    ))



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

        self._all_regex_groups: List[str] = sorted(list(all_regex_groups))

        # Populate a map between each unique group in the field and a unique
        # integer that is guarenteed to be a safe sql name.
        for group_index, group_name in enumerate(self._all_regex_groups):
            self._regex_group_to_index[group_name] = group_index

    ############################################################################
    # regex_field_patterns
    #
    # A helper function to return the dict cache of compiled regexess that this
    # producer uses.
    ############################################################################
    def regex_field_patterns(self) -> Dict[str, "re.Pattern[str]"]:
        return self._compiled_regexes

    def get_all_match_groups(self) -> List[str]:
        return self._all_regex_groups

    def get_match_groups(self, field_name: str) -> List[str]:
        return self._regex_groups[field_name]

    def get_match_group_id(self, group_name: str) -> str:
         return str(self._regex_group_to_index[group_name])

    # ############################################################################
    # # get_field_table_name
    # #
    # # A helper function to produce the name of the table that stores matches
    # # for a particular field.
    # # TODO: The SQL logic should somehow be moved to scheduler.py
    # ############################################################################
    # @staticmethod
    # def get_field_table_name(producer_index: int, field_index: int) -> str:
    #     return "producer{producer_index}_field{field_index}_matches".format(producer_index=producer_index, field_index=field_index)


    def get_field_id(self, field_name: str) -> str:
        return str(self._field_to_field_id[field_name])


    def input_path_patterns_dict(self) -> Dict[str, Union[str, List[str]]]:
        # Ignoring this type because we are returning a TypedDict that is of
        # this specified type, however python typechecking cannot validate
        # that a TypedDict is also a Dict it seems.
        return self._input_path_patterns # type:ignore


# Convenience type to get around making lists of Producers with different
# arguments.
GenericProducer = Producer[Any, Any]
