from typing import List, Callable, Any, Optional, Union, Set, Tuple
from collections import deque
from dataclasses import dataclass
import heapq
import re
import os
import sys


@dataclass
class Producer():
    # A list of file regex matches. If a file is changed that matches one of
    # these regex matches then this producer will trigger 
    input_path_patterns: List[str]

    # A list output files or a function to transform an input file into a list
    # of output files. The function will receive the path of the modified file
    # in as an input.
    output_paths: Callable[[str, re.Match], List[str]]


    function: Callable[[str, re.Match, List[str]], None]

    # # A function that handles its own monitoring and updating logic. For example
    # # the `tsc` typescript compiler.
    # self_watcher_function: Optional[Callable[[], Any]]

    # To take advantage of hot retriggering of some expensive-to-start javascript commands like tsc
    # self_watch_function: Optional[Callable[], Any]

    # TODO: This should probably be a generator function too...
    categories: List[str]

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

################################################################################
# Runs each producer over all of the files 
# TODO: Setup watchers for each input file

# Runs each producer if any of the input files are newer then any of the output files
# Each producer is run in order and dependency tree mapping is not done.
# NOTE: this is kinda ironic becuase doing dependency tree mapping would be very
# similar to what the calculator actually does.
################################################################################
def build_producer_calls(producers: List[Producer], ignore_paths: List[str]):
    # TODO: something around checking if this code has been updated at all
    # and restarting it or something...

    paths: List[str] = []

    for root, dirs, files in os.walk("."):
        # Strip the "current directory" prefix because that makes it more
        # annoying to match things on.
        if root.startswith("./"):
            root = root[2:]

        for path in dirs + files:
            full_path = os.path.join(root, path)
            
            skip = False
            for ignore_path in ignore_paths:
                if full_path.startswith(ignore_path):
                    skip = True
                    break
            if skip:
                continue

            paths.append(full_path)

    # A list of all the producers and path combinations that still need to be processed
    producer_paths: List[Tuple[int, str]] = []
    for producer_index, _ in enumerate(producers):
        for path in paths:
            heapq.heappush(producer_paths, (producer_index, path))


    while len(producer_paths) > 0:
        producer_path: Tuple[int, str] = heapq.heappop(producer_paths)
        producer_index: int = producer_path[0]
        producer: Producer = producers[producer_path[0]]
        path: str = producer_path[1]

        for pattern in producer.input_path_patterns:
            match: Optional[re.Match[str]] = re.match(pattern, path)
           
            # Ignore this pattern/file if there is no match
            if match is None:
                continue

            output_files: List[str] = producer.output_paths(path, match)
            all_output_files_exist = True
            for output_file in output_files:
                if not os.path.exists(output_file):
                    all_output_files_exist = False
                    break

            if all_output_files_exist:
                # If all of the output files are newer then all of the input files
                # then do not regenerate this producer.
                oldest_output = get_oldest_modified_time(output_files)
                newest_input = get_newest_modified_time([path])
                # "newer" is a larger number
                if oldest_output > newest_input:
                    continue


            # Add the output files to the prioritized list of things to process.
            # These will be automatically deduplicated if they are already
            # present.
            for producer_index, _ in enumerate(producers):
                for output_file in output_files:
                    heapq.heappush(producer_paths, (producer_index, output_file))

            build_required_directories(output_files)




            print(producer.categories, path, pattern, output_files)



            producer.function(path, match, output_files)
            # print("bringing it back")

            # If one pattern has matched by this point then there is no
            # need to continue searching for patterns because we would just
            # re-call the file.
            break


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
