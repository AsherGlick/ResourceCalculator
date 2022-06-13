from typing import List, Callable, Any, Optional, Union, Set, Tuple, TypeVar, Generic, Dict
from collections import deque
from dataclasses import dataclass
import heapq
import re
import os
import sys


InputFileDatatype = Dict[str, Union[str, List[str]]]
OutputFileDatatype = Dict[str, str]

class Creator:
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

            # elif isinstance(input_path, list) and all([isinstance(x, str) for x in input_path]):
            #     for sub_input_path in self.input_path:
            #         self._flat_input_paths.add(sub_input_path)

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

@dataclass
class Producer:
    # A list of file regex matches. If a file is changed that matches one of
    # these regex matches then this producer will trigger 
    input_path_patterns: List[str]

    paths: Callable[[int, str, re.Match], Tuple[InputFileDatatype, OutputFileDatatype]]

    # # A list output files or a function to transform an input file into a list
    # # of output files. The function will receive the path of the modified file
    # # in as an input.
    # output_paths: Callable[[str, re.Match], List[str]]

    # A function that takes in
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

    # _unique_id: str

    # def __init__(self,
    #     input_path_patterns: List[str],
    #     output_paths: Callable[[str, re.Match], List[str]],
    #     function: Callable[[str, List[str]], None],
    #     categories: List[str]
    # ):
    #     self.input_path_patterns = input_path_patterns
    #     self.output_paths = output_paths
    #     self.function = function
    #     self.categories = categories

    #     # Create a unique id that we can use as a hashable value
    #     global producer_count
    #     self._unique_id = str(__class__) + str(producer_count)
    #     producer_count += 1

    @staticmethod
    def static_output(output_file: str) -> Callable[[str, re.Match], List[str]]:
        def output(path: str, match: re.Match) -> List[str]:
            return [output_file]
        return output

# A controller and watcher for the set of producers and creators
class Studio:
    producer_list: List[Producer]
    creator_list: List[Tuple[int, Creator]] # is this actually a heapq

    def __init__(self, producer_list: List[Producer], ignore_paths: List[str] = []):
        self.producer_list = producer_list
        self.creator_list = []

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

        self.add_files(initial_filepaths)


    def add_files(self, files: List[str]):
        # Build any new Creators based on the files
        for producer_index, producer in enumerate(self.producer_list):
            for path in files:
                for pattern_index, pattern in enumerate(producer.input_path_patterns):
                    match: Optional[re.Match[str]] = re.match(pattern, path)
        
                    # Ignore this pattern/file if there is no match
                    if match is None:
                        continue

                    input_paths, output_paths = producer.paths(pattern_index, pattern, match)

                    creator = Creator(
                        input_paths=input_paths,
                        output_paths=output_paths,
                        function=producer.function,
                        categories=producer.categories(input_paths)
                    )

                    # print("We have a match")
                    # print("  ", producer_index)
                    # print("  ", producer)
                    # print("  ", creator)
                    # print("  ", path)
                    # print("  ", pattern)

                    heapq.heappush(self.creator_list, (producer_index, creator))


        # Trigger a file update for all the new files
        self.update_files(files)

    # def delete_files(self, files: List[str]):
    #     pass

    def update_files(self, files: List[str]):
        creators_to_update: List[Tuple[int, Creator]] = [] # actually a heap

        for file in files:
            for producer_index, creator in self.creator_list:
                if(creator.has_input(file)):
                    heapq.heappush(creators_to_update, (producer_index, creator))

        while len(creators_to_update) > 0:
            producer_index, creator = heapq.heappop(creators_to_update)

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
            # These will be automatically deduplicated if they are already
            # present.
            for file in output_files:
                for producer_index, re_creator in self.creator_list:
                    if(re_creator.has_input(file)):
                        heapq.heappush(creators_to_update, (producer_index, re_creator))


            # Pre-create any directories so the functions can always assume that
            # the directories exist and just focus on creating the files.
            build_required_directories(output_files)

            print(creator.categories, input_files, output_files)
            creator.run()




def all_files_exist(files: List[str]) -> bool:
    for file in files:
        if not os.path.exists(file):
            return False
    return True


# ################################################################################
# # Runs each producer over all of the files 
# # TODO: Setup watchers for each input file

# # Runs each producer if any of the input files are newer then any of the output files
# # Each producer is run in order and dependency tree mapping is not done.
# # NOTE: this is kinda ironic becuase doing dependency tree mapping would be very
# # similar to what the calculator actually does.
# ################################################################################
# def build_producer_calls(producers: List[Producer], ignore_paths: List[str]):
#     # TODO: something around checking if this code has been updated at all
#     # and restarting it or something...

#     paths: List[str] = []

#     for root, dirs, files in os.walk("."):
#         # Strip the "current directory" prefix because that makes it more
#         # annoying to match things on.
#         if root.startswith("./"):
#             root = root[2:]

#         for path in dirs + files:
#             full_path = os.path.join(root, path)
            
#             skip = False
#             for ignore_path in ignore_paths:
#                 if full_path.startswith(ignore_path):
#                     skip = True
#                     break
#             if skip:
#                 continue

#             paths.append(full_path)

#     # A list of all the producers and path combinations that still need to be processed
#     producer_paths: List[Tuple[int, str]] = []
#     for producer_index, _ in enumerate(producers):
#         for path in paths:
#             heapq.heappush(producer_paths, (producer_index, path))


#     while len(producer_paths) > 0:
#         producer_path: Tuple[int, str] = heapq.heappop(producer_paths)
#         producer_index: int = producer_path[0]
#         producer: Producer = producers[producer_path[0]]
#         path: str = producer_path[1]

#         for pattern in producer.input_path_patterns:
#             match: Optional[re.Match[str]] = re.match(pattern, path)
           
#             # Ignore this pattern/file if there is no match
#             if match is None:
#                 continue

#             output_files: List[str] = producer.output_paths(path, match)
#             all_output_files_exist = True
#             for output_file in output_files:
#                 if not os.path.exists(output_file):
#                     all_output_files_exist = False
#                     break

#             if all_output_files_exist:
#                 # If all of the output files are newer then all of the input files
#                 # then do not regenerate this producer.
#                 oldest_output = get_oldest_modified_time(output_files)
#                 newest_input = get_newest_modified_time([path])
#                 # "newer" is a larger number
#                 if oldest_output > newest_input:
#                     continue


#             # Add the output files to the prioritized list of things to process.
#             # These will be automatically deduplicated if they are already
#             # present.
#             for producer_index, _ in enumerate(producers):
#                 for output_file in output_files:
#                     heapq.heappush(producer_paths, (producer_index, output_file))

#             build_required_directories(output_files)




#             print(producer.categories, path, pattern, output_files)



#             producer.function(path, match, output_files)
#             # print("bringing it back")

#             # If one pattern has matched by this point then there is no
#             # need to continue searching for patterns because we would just
#             # re-call the file.
#             break


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
