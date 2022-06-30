from typing import List, Callable, Any, Optional, Union, Set, Tuple, TypeVar, Generic, Dict
from collections import deque
from dataclasses import dataclass
import heapq
import re
import os
import sys
from typing import TypedDict

from pylib.unique_heap import UniqueHeap
import time
import shutil
from .producer import Producer, GenericProducer
from .creator import Creator
import sqlite3


GenericCreator = Creator[Any, Any]

################################################################################
# Scheduler is a tool for scheduling jobs to be completed based on the
# existence and modification of files.
################################################################################


################################################################################
# A controller and watcher for the set of producers and creators
################################################################################
class Scheduler:
    # A list of producers that can be referenced by id
    producer_list: List[GenericProducer]

    # A list of creators that can be referenced by id
    creator_list: Dict[int, GenericCreator]
    last_creator_list_index: int

    # A map of a creator index to a producer index that spawned the creator
    creator_producer: Dict[int, int]

    # A map of output files to the creator indexes that create them
    output_file_maps: Dict[str, int]

    # A map of input files to the creator index that consume them
    input_file_maps: Dict[str, List[int]]


    ############################################################################
    #
    ############################################################################
    def __init__(
        self,
        producer_list: List[GenericProducer],
        initial_filepaths: List[str] = []
    ):
        self.producer_list = producer_list
        self.creator_list = {}
        self.last_creator_list_index = -1
        self.creator_producer = {}
        self.output_file_maps = {}
        self.input_file_maps = {}

        self.filecache: sqlite3.Connection = self.init_producer_cache(self.producer_list)
        self.add_or_update_files(initial_filepaths)

    def init_producer_cache(self, producer_list: List[GenericProducer]) -> sqlite3.Connection:
        db = sqlite3.connect(':memory:')

        for producer_index, producer in enumerate(producer_list):
            for init_query in producer.init_table_query(producer_index):
                with db:
                    db.execute(init_query)

        return db


    ############################################################################
    # add_or_update_files
    #
    # This function should be called whenever a file is added to the source
    # tree, or updated inside the source tree. It should be called with a list
    # of all files on program initialization.
    ############################################################################
    def add_or_update_files(self, files: List[str]) -> None:
        self.build_new_creators(files)
        self.process_files(files)

    def build_new_creators(self, files: List[str]) -> None:
        for producer_index, producer in enumerate(self.producer_list):
            for path in files:
                for field_name, pattern in producer.regex_field_patterns().items():
                    match: Optional[re.Match[str]] = re.match(pattern, path)

                    if match is None:
                        continue

                    producer.insert(self.filecache, producer_index, field_name, path, match.groupdict())

        # Build a list of creators
        for producer_index, producer in enumerate(self.producer_list):
            input_datas = producer.query_filesets(self.filecache, producer_index)
            for input_data in input_datas:
                input_file, input_groups = input_data
                # print(input_file, input_groups)

                new_input_data, output_data = producer.paths(input_file, input_groups)

                categories = producer.categories

                if callable(categories):
                    categories = categories(new_input_data, output_data)

                creator = Creator(
                    input_paths=new_input_data,
                    output_paths=output_data,
                    function=producer.function,
                    categories=categories
                )

                # Detect duplicate creators
                # TODO: no duplicate creators should exist at all given this
                # even ones that have identical producers, inputs, and outputs.
                # Eventually this check should be much stricter.
                is_duplicate_creator = False
                for file in creator.flat_output_paths():
                    if file in self.output_file_maps:
                        is_duplicate_creator = True
                        original_creator_index: int = self.output_file_maps[file]
                        original_creator: GenericCreator = self.creator_list[original_creator_index]

                        if (sorted(original_creator.flat_input_paths()) != sorted(creator.flat_input_paths())):
                            raise ValueError("Two creators with same output file do not share all input files")

                        if (sorted(original_creator.flat_output_paths()) != sorted(creator.flat_output_paths())):
                            raise ValueError("Two creators with same output file do not share all output files")

                        if producer_index != self.creator_producer[original_creator_index]:
                            raise ValueError("Two creators with same output file are not made from the same")
                        # print("Duplicate creator found with the same data. Deduplicating.")
                if is_duplicate_creator:
                    continue


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
    # process_files
    #
    #
    ############################################################################
    def process_files(self, files: List[str]) -> None:
        # Heap[Tuple[ProducerIndex, CreatorIndex]]
        creators_to_update: UniqueHeap[Tuple[int, int]] = UniqueHeap()

        # Fill the creators_to_update will all the producer/creator pairs
        for file in files:
            # If the file is not used in any creator, ignore it
            if file not in self.input_file_maps:
                continue

            creator_indexes: List[int] = self.input_file_maps[file]
            for creator_index in creator_indexes:
                producer_index: int = self.creator_producer[creator_index]
                creators_to_update.push((producer_index, creator_index))

        # Process each creator until there are none left
        while len(creators_to_update) > 0:
            producer_index, creator_index = creators_to_update.pop()

            creator: GenericCreator = self.creator_list[creator_index]

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
            # self.make_creators(output_files)
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
            start = time.time()
            creator.run()
            duration = time.time() - start
            print("  Completed in {:.2f}".format(duration))



    ############################################################################
    # all_paths_in_dir
    #
    # A helper function to use for initial_filepaths when you want to add all
    # of the files under a particular directory.
    ############################################################################
    @staticmethod
    def all_paths_in_dir(base_dir: str, ignore_paths: List[str]) -> List[str]:
        paths: List[str] = []

        for root, dirs, files in os.walk(base_dir):
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

                paths.append(full_path)

        return paths



################################################################################
# all_files_exist
#
# A helper function that will check if every file in a list exist. If one or
# more files does not exist then it will return False. If an empty list is
# passed in then it will return True.
################################################################################
def all_files_exist(files: List[str]) -> bool:
    for file in files:
        if not os.path.exists(file):
            return False
    return True


################################################################################
# build_required_directories
#
# Takes in a list of files and then creates all of the directories needed in
# order for those files to be written to if they do not already exist.
################################################################################
def build_required_directories(files: List[str]) -> None:
    for file in files:
        directory = os.path.dirname(file)
        if not os.path.exists(directory):
            os.makedirs(directory)


################################################################################
# get_newest_modified_time
#
# This function takes in a list of files and returns the most recent time any
# of them were modified.
################################################################################
def get_newest_modified_time(paths: List[str]) -> float:
    return get_aggregated_modified_time(
        paths=paths,
        aggregator=max,
        default=sys.float_info.max,
    )


################################################################################
# get_oldest_modified_time
#
# This function takes in a list of files and returns the least recent time any
# of them were modified.
################################################################################
def get_oldest_modified_time(paths: List[str]) -> float:
    return get_aggregated_modified_time(
        paths=paths,
        aggregator=min,
        default=0,
    )


################################################################################
# get_aggregated_modified_time
#
# A helper function for get_newest_modified_time() and get_oldest_modified_time()
# which use almost identical logic save for the default values of non existent
# files, and the aggregator function used over all of the file ages.
################################################################################
def get_aggregated_modified_time(
    paths: List[str],
    aggregator: Callable[[List[float]], float],
    default: float
) -> float:
    # Duplicate the paths list so we can modify it. This allows us to avoid
    # recursion by just appending the values 
    paths = list(paths)
    time_list: List[float] = []
    for path in paths:
        # If a path is missing add the default value instead
        if not os.path.exists(path):
            time_list.append(default)
            continue

        # If a path is a directory add all its children to the paths list
        if (os.path.isdir(path)):
            for subpath in os.listdir(path):
                paths.append(os.path.join(path, subpath))
        else:
            time_list.append(os.path.getctime(path))

    # Sanity check that there are timestamps in the list before passing them
    # to the aggregator.
    if len(time_list) == 0:
        return default

    return aggregator(time_list)
