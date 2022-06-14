from typing import List, Callable, Any, Optional, Union, Set, Tuple, TypeVar, Generic, Dict
from collections import deque
from dataclasses import dataclass
import heapq
import re
import os
import sys
from typing import TypedDict

from pylib.unique_heap import UniqueHeap



# Convenience Class for anything with a single input or output file
class SingleFile(TypedDict):
    file: str

# Convenience Class for anything with a single group of input or output files
class MultiFile(TypedDict):
    files: List[str]


# def core_categories(input_files: InputFileDatatype) -> List[str]:
#     return ["core", input_files["input"]]

# def core_resource_paths(index: int, regex: str, match: re.Match) -> Tuple[InputFileDatatype, OutputFileDatatype]:
#     return ({
#             "input": match.group(0)
#         },{
#             "output": os.path.join("output", os.path.basename(match.group(0)))
#         })
    
# def producer_copyfile(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:



InputFileDatatype = TypeVar("InputFileDatatype", bound=TypedDict)
OutputFileDatatype = TypeVar("OutputFileDatatype", bound=TypedDict)

################################################################################
# Creator
#
# This is a static pairing of input files to output files. These are
# constructed and managed fully behind the scenes and should not be implemented
# by users directly. Producers are in charge of constructing them and Studios
# are in charge of managing them after their creation.
################################################################################
class Creator(Generic[InputFileDatatype, OutputFileDatatype]):
    input_paths: InputFileDatatype
    _input_paths_set: Set[str]
    output_paths: OutputFileDatatype
    function: Callable[[InputFileDatatype, OutputFileDatatype], None]
    categories: List[str]

    ############################################################################
    ############################################################################
    def __init__(
        self,
        input_paths: InputFileDatatype,
        output_paths: OutputFileDatatype,
        function: Callable[[InputFileDatatype, OutputFileDatatype], None],
        categories: List[str],
    ):
        self.input_paths = input_paths
        self.output_paths = output_paths
        self.function = function
        self.categories = categories

        # Pre-cache the input files in a set for very fast file lookups.
        self._input_paths_set = set(self.flat_input_paths())


    ############################################################################
    ############################################################################
    def __repr__(self) -> str:
        return "Creator(input_files={}, output_paths={}, function={}, categories={})".format(
            str(self.input_paths),
            str(self.output_paths),
            str(self.function),
            str(self.categories)
        )

    ############################################################################
    ############################################################################
    def flat_input_paths(self) -> List[str]:
        flat_input_paths: List[str] = []
        for input_path in self.input_paths.values():
            if isinstance(input_path, str):
                flat_input_paths.append(input_path)

            elif isinstance(input_path, list) and all([isinstance(x, str) for x in input_path]):
                for sub_input_path in input_path:
                    flat_input_paths.append(sub_input_path)

            else:
                raise TypeError("Expected either a string or a list of strings but got", input_path)

        return flat_input_paths


    ############################################################################
    ############################################################################
    def flat_output_paths(self) -> List[str]:
        flat_output_paths: List[str] = []
        for output_path in self.output_paths.values():
            if isinstance(output_path, str):
                flat_output_paths.append(output_path)

            elif isinstance(output_path, list) and all([isinstance(x, str) for x in output_path]):
                for sub_output_path in output_path:
                    flat_output_paths.append(sub_output_path)

            else:
                raise TypeError("Expected either a string but got", output_path)

        return flat_output_paths

    ############################################################################
    ############################################################################
    def has_input(self, input_path: str) -> bool:
        return input_path in self._input_paths_set


    ############################################################################
    ############################################################################
    def run(self):
        self.function(self.input_paths, self.output_paths)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Creator):
            raise TypeError("'<' not supported between instances of 'Creator' and {}".format(type(other)))

        self_paths = [sorted(self.flat_output_paths()), sorted(self.flat_input_paths())]
        other_paths = [sorted(other.flat_output_paths()), sorted(other.flat_input_paths())]

        return self_paths < other_paths

@dataclass
class Producer(Generic[InputFileDatatype, OutputFileDatatype]):
    # A list of file regex matches. If a file is changed that matches one of
    # these regex matches then this producer will trigger 
    input_path_patterns: List[str]

    # A function that takes in the matching input pattern and generates a set
    # of input and output files.
    paths: Callable[[int, str, re.Match], Tuple[InputFileDatatype, OutputFileDatatype]]

    # A function that takes in the input and output files and performs the
    # tasks required to transform the input files into output files.
    function: Callable[[InputFileDatatype, OutputFileDatatype], None]

    # # A function that handles its own monitoring and updating logic. For example
    # # the `tsc` typescript compiler.
    # self_watcher_function: Optional[Callable[[], Any]]

    # To take advantage of hot retriggering of some expensive-to-start javascript commands like tsc
    # self_watch_function: Optional[Callable[], Any]

    # TODO: This should probably be a generator function too...
    # categories: List[str]
    categories: Callable[[InputFileDatatype], List[str]]

    # an alternative for "function" that will be called if this step is to be skipped
    # EG: javascript minification would have a simple copyfunction here because
    #     the file(s) still need to exist at the destination.
    # fast_function: Optional[Callable[[str, List[str]], None]] = None


# A controller and watcher for the set of producers and creators
class Studio:
    # A list of producers that can be referenced by id
    producer_list: List[Producer]

    # A list of creators that can be referenced by id
    creator_list: Dict[int, Creator]
    last_creator_list_index: int

    # A map of a creator index to a producer index that spawned the creator
    creator_producer: Dict[int, int]

    # A map of output files to the creator indexes that create them
    output_file_maps: Dict[str, int]
    # A map of input files to the creator index that consume them
    input_file_maps: Dict[str, List[int]]

    def __init__(self, producer_list: List[Producer], ignore_paths: List[str] = []):
        self.producer_list = producer_list
        self.creator_list = {}
        self.last_creator_list_index = -1
        self.creator_producer = {}
        self.output_file_maps = {}
        self.input_file_maps = {}

        # Grab all of the files that are in the directory as if they are all
        # new to the builder.
        initial_filepaths: List[str] = []
        for root, dirs, files in os.walk("."):
            # Strip the "current directory" prefix because that makes it more
            # annoying to match things on.
            if root.startswith("./"):
                root = root[2:]

            # Add all of the files and directories unless the path matches an ignore path
            for path in dirs + files:
                full_path = os.path.join(root, path)
                
                skip = False
                for ignore_path in ignore_paths:
                    if full_path.startswith(ignore_path):
                        skip = True
                        break
                if skip:
                    continue

                initial_filepaths.append(full_path)

        self.update_files(initial_filepaths)


    # TODO: This should probably just be part of "update_files" and if a file
    # that has never been seen before is passed in then the new file logic is
    # triggered automatically.
    def make_creators(self, files: List[str]):
        # Build any new Creators based on the files
        for producer_index, producer in enumerate(self.producer_list):
            for path in files:
                for pattern_index, pattern in enumerate(producer.input_path_patterns):
                    match: Optional[re.Match[str]] = re.match(pattern, path)
        
                    # Ignore this pattern/file if there is no match
                    if match is None:
                        continue

                    input_paths, output_paths = producer.paths(pattern_index, pattern, match)

                    # Create the creator
                    creator = Creator(
                        input_paths=input_paths,
                        output_paths=output_paths,
                        function=producer.function,
                        categories=producer.categories(input_paths)
                    )

                    is_duplicate_creator = False
                    # Detect duplicate creators or overlapping creators 
                    for file in creator.flat_output_paths():
                        if file in self.output_file_maps:
                            is_duplicate_creator = True
                            original_creator_index: int = self.output_file_maps[file]
                            original_creator: Creator = self.creator_list[original_creator_index]

                            if (sorted(original_creator.flat_input_paths()) != sorted(creator.flat_input_paths())):
                                raise ValueError("Two creatos with same output file do not share all input files")

                            if (sorted(original_creator.flat_output_paths()) != sorted(creator.flat_output_paths())):
                                raise ValueError("Two creators with same output file do not share all output files")

                            if producer_index != self.creator_producer[original_creator_index]:
                                raise ValueError("Two creators with same output file are not made from the same")

                            print("Duplicate Found with same data", file)
                    if is_duplicate_creator:
                        continue

                    # Save the new creator into this studio
                    self.last_creator_list_index += 1
                    self.creator_list[self.last_creator_list_index] = creator
                    self.creator_producer[self.last_creator_list_index] = producer_index

                    for file in creator.flat_input_paths():

                        if file not in self.input_file_maps:
                            self.input_file_maps[file] = []

                        self.input_file_maps[file].append(self.last_creator_list_index)

                    for file in creator.flat_output_paths():
                        self.output_file_maps[file] = self.last_creator_list_index


    ############################################################################
    #
    ############################################################################
    def update_files(self, files: List[str]):

        self.make_creators(files)

        # Heap[Tuple[ProducerIndex, CreatorIndex]]
        creators_to_update: UniqueHeap[Tuple[int, int]] = UniqueHeap()

        # Fill the creators_to_update will all the producer/creator pairs
        for file in files:
            # If the file is not used in any creator, ignore it
            if file not in self.input_file_maps:
                continue

            # print(file, file in self.input_file_maps)

            creator_indexes: List[int] = self.input_file_maps[file]
            for creator_index in creator_indexes:
                producer_index: int = self.creator_producer[creator_index]
                creators_to_update.push((producer_index, creator_index))

        # Process each creator until there are none left
        while len(creators_to_update) > 0:
            producer_index, creator_index = creators_to_update.pop()

            creator: Creator = self.creator_list[creator_index]

            output_files = creator.flat_output_paths()
            input_files = creator.flat_input_paths()

            if all_files_exist(creator.flat_output_paths()):
                # If all of the output files are newer then all of the input files
                # then do not regenerate this producer.
                oldest_output = get_oldest_modified_time(output_files)
                newest_input = get_newest_modified_time(input_files)
                # "newer" is a larger number
                if oldest_output > newest_input:
                    continue

            # Add the output files to the prioritized list of things to process.
            # These will be automatically de-duplicated if they are already present.
            self.make_creators(output_files)
            for file in output_files:
                # If the file is not used in any creator, ignore it
                if file not in self.input_file_maps:
                    continue

                creator_indexes: List[int] = self.input_file_maps[file]
                for creator_index in creator_indexes:
                    producer_index: int = self.creator_producer[creator_index]
                    creators_to_update.push((producer_index, creator_index))

            # Pre-create any directories so the functions can always assume that
            # the directories exist and just focus on creating the files.
            build_required_directories(output_files)

            # print(creator.categories, input_files, output_files)
            print(creator.categories, output_files)
            creator.run()




def all_files_exist(files: List[str]) -> bool:
    for file in files:
        if not os.path.exists(file):
            return False
    return True


def build_required_directories(files: List[str]) -> None:
    for file in files:
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)


################################################################################
# get_newest_modified_time
#
# This function takes in a list of files and returns the newest time any of
# them were modified.
################################################################################
def get_newest_modified_time(paths: List[str]) -> float:
    return get_ist_modified_time(
        paths=paths,
        ist=min,
        default=sys.float_info.max,
    )

def get_oldest_modified_time(paths: List[str]) -> float:
    return get_ist_modified_time(
        paths=paths,
        ist=min,
        default=0,
    )

def get_ist_modified_time(paths: List[str], ist: Callable[[List[float]], float], default: float) -> float:
    # Duplicate the paths list so we can modify it
    paths = list(paths)
    time_list: List[float] = []
    for path in paths:
        if (os.path.isdir(path)):
            for subpath in os.listdir(path):
                paths.append(os.path.join(path, subpath))
        else:
            time_list.append(os.path.getctime(path))

    if len(time_list) == 0:
        return default

    return ist(time_list)    
