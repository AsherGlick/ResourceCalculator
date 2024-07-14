################################################################################
# Scheduler is a tool for scheduling jobs to be completed based on the
# existence and modification of files.
################################################################################
import shutil
from typing import List, Callable, Any, Optional, Tuple, Dict, Set, Generic, Union
import os
import re
import sqlite3
import sys
import time
import json

from .producer import GenericProducer
from .producer import InputFileDatatype
from dataclasses import dataclass, field
from pylib.terminal_color import fg_gray
from pylib.unique_heap import UniqueHeap


BUILD_EVENTS_FILE = ".buildevents.json"
TEMPORARY_BUILD_EVENTS_FILE = ".buildevents.json.tmp"

# A record of a build event taking a set of input files, a producer, and a set of output files
@dataclass
class BuildEvent:
    producer_name: str
    input_files: List[str]
    match_groups: Dict[str, str]
    output_files: List[str]

    # We can store any warnings in the build log so that when a step is skipped
    # subsequent runs we can still remind the user that there were errors when
    # that step was run previously.
    # warnings: List[str]

    def weak_hash(self) -> int:
        return hash(tuple(
            [self.producer_name]
            + sorted([(k, v) for k, v in self.match_groups.items()])
        ))


@dataclass
class Action(Generic[InputFileDatatype]):
    producer_index: int
    producer_name: str
    input_files: InputFileDatatype
    match_groups: Dict[str, str]

    ############################################################################
    # producer
    #
    # A helper function to get the producer object from the internal producer
    # index variable.
    ############################################################################
    def producer(self, producer_list: List[GenericProducer]):
        return producer_list[self.producer_index]

    ############################################################################
    # files
    #
    # Returns a flat sorted flat tuple containing all of the files of this
    ############################################################################
    def files(self) -> Tuple[str, ...]:
        files: List[str] = []
        for input_file in self.input_files.values():
            if isinstance(input_file, str):
                files.append(input_file)
            elif isinstance(input_file, list):
                files += input_file
            else:
                raise TypeError
        return tuple(sorted(files))

    ############################################################################
    # Comparison functions
    ############################################################################
    def __lt__(self, other: "Action"):
        return self.producer_index < other.producer_index
    def __gt__(self, other: "Action"):
        return self.producer_index > other.producer_index
    def __le__(self, other: "Action"):
        return self.producer_index <= other.producer_index
    def __ge__(self, other: "Action"):
        return self.producer_index >= other.producer_index

    ############################################################################
    # weak_hash
    #
    # A hash function that hashes the producer and the match groups.
    ############################################################################
    def weak_hash(self) -> int:
        return hash(tuple(
            [self.producer_name]
            + sorted([(k, v) for k, v in self.match_groups.items()])
        ))


################################################################################
# A controller and watcher for the set of producers and creators
################################################################################
class Scheduler:
    # A list of producers that can be referenced by id
    producer_list: List[GenericProducer]

    # A list of all of the build events that have occurred in this scheduler
    # run, or maybe this is a list of all valid build events from the past run
    # eg: ones where the output files have not been changed or delted since they ran
    build_events: List[Optional[BuildEvent]]

    # A map of filename -> Set of `producer_list` indexes
    input_file_maps: Dict[str, Set[Action]]

    # A datastructure that holds information about all of the currently known files
    filecache: sqlite3.Connection

    ############################################################################
    # 
    ############################################################################
    def __init__(
        self,
        producer_list: List[GenericProducer],
        initial_filepaths: List[str] = []
    ):
        # Check that every producer has a unique name.
        producer_names: Set[str] = set()
        for producer in producer_list:
            if producer.name in producer_names:
                raise ValueError("Duplicate producer name found {}. Every producer must have a unique name.".format(producer.name))
            else:
                producer_names.add(producer.name)

        self.producer_list = producer_list

        self.filecache = self.init_producer_cache(self.producer_list)

        self.load_build_events()
        self._process_files(initial_filepaths, init=True)

    ############################################################################
    # add_or_update_files
    #
    # This function is called whenever a file is added to the source tree, or
    # updated inside the source tree.
    ############################################################################
    def add_or_update_files(self, files: List[str]) -> None:
        self._process_files(files)


    # Load the build events into the class
    def load_build_events(self) -> None:
        self.build_events = []
        raw_build_events = self._read_build_events_file()

        for raw_build_event in raw_build_events:
            # TODO: Replace this with classnotation
            build_event: BuildEvent = BuildEvent(
                producer_name=raw_build_event["producer_name"],
                input_files=raw_build_event["input_files"],
                match_groups=raw_build_event["match_groups"],
                output_files=raw_build_event["output_files"],
            )
            self.build_events.append(build_event)

    # A seperate function for reading build_event files from disk to support mocking in unit tests
    def _read_build_events_file(self) -> Any:
        if not os.path.exists(BUILD_EVENTS_FILE):
            return []
        with open(BUILD_EVENTS_FILE, "r") as f:
            return json.load(f)

    # Save the build events currently in the class
    def save_build_events(self) -> None:
        raw_build_events: List[Dict[str, Any]] = []
        for build_event in self.build_events:
            if build_event is None:
                continue
            raw_build_events.append({
                "producer_name": build_event.producer_name,
                "input_files": build_event.input_files,
                "match_groups": build_event.match_groups,
                "output_files": build_event.output_files,
            })
        self._write_build_events_file(raw_build_events)


    # A seperate function for writing build_event files to disk to support mocking in unit tests
    def _write_build_events_file(self, data: Any) -> None:
        with open(TEMPORARY_BUILD_EVENTS_FILE, "w") as f:
            json.dump(data, f)
        shutil.move(TEMPORARY_BUILD_EVENTS_FILE, BUILD_EVENTS_FILE)



    ############################################################################
    # _add_files_to_database
    #
    # Matches each file against the all of the producer regexes to see if there
    # are any matches. If there are then the file is added to the db as a part
    # of the match. A file can be added multiple times if there are multiple
    # matches found.
    ############################################################################
    def _add_files_to_database(self, files: List[str]) -> None:
        # Insert or update all files in the database
        for producer_index, producer in enumerate(self.producer_list):
            for path in files:
                for field_name, pattern in producer.regex_field_patterns().items():
                    match: Optional[re.Match[str]] = re.match(pattern, path)
                    if match is None:
                        continue

                    # Delete the file from the database if it exists
                    self.remove_file_from_database(
                        self.filecache,
                        producer_index,
                        field_name,
                        path
                    )

                    # Insert a file into the database. If it already exists then
                    # it is updated to be marked as a fresh file.
                    self.insert_new_file(
                        self.filecache,
                        producer_index,
                        field_name,
                        path,
                        match.groupdict()
                    )

    ############################################################################
    # _query_for_actions_from_files
    #
    # Query the database for all of the actions relevent to the list of filter
    # files, and returns those action objects.
    ############################################################################
    def _query_for_actions_from_files(self, filter_files: List[str]) -> List[Action]:
        actions: List[Action] = []
        for producer_index, producer in enumerate(self.producer_list):
            queried_actions = self.query_filesets(self.filecache, producer_index)
            for queried_action in queried_actions:
                inputs, input_groups = queried_action

                action = Action(
                    producer_index=producer_index,
                    producer_name=producer.name,
                    input_files=inputs,
                    match_groups=input_groups
                )

                # Only add this action if it has one of the input_files as an input file
                for file in action.files():
                    if file in filter_files:
                        actions.append(action)
                        break
        return actions

    ############################################################################
    # get_actions_with_quasifiles
    #
    # Get a list of actions that would have changed if the quasifiles existed.
    ############################################################################
    def get_actions_with_from_quasifiles(self, quasifiles: List[str]) -> List[Action]:
        quasiactions: List[Action] = []
        for quasifile in quasifiles:
            for producer_index, producer in enumerate(self.producer_list):
                quasigroups: Dict[str, str] = {}

                for _, pattern in producer.regex_field_patterns().items():
                    match: Optional[re.Match[str]] = re.match(pattern, quasifile)
                    if match is None:
                        continue
                    for group, value in match.groupdict().items():
                        quasigroups[group] = value
                queried_actions = self.query_filesets(self.filecache, producer_index)

                for queried_action in queried_actions:
                    action_inputs = queried_action[0]
                    action_groups: Dict[str, str] = queried_action[1]

                    # Check if this is an action we want becuase it matches the quasigroups
                    if quasigroups == action_groups:
                        quasiactions.append(Action(
                            producer_index=producer_index,
                            producer_name=producer.name,
                            input_files=action_inputs,
                            match_groups=action_groups
                        ))

        return quasiactions

    ############################################################################
    # _process_files
    #
    # Takes in a list of files that have been created or modified and then
    # runs all of the producer functions that would take in any of those files.
    ############################################################################
    def _process_files(self, files: List[str], init: bool=False) -> None:
        actions_to_run: UniqueHeap[Action] = UniqueHeap()

        # Delete a build event and the files associated with it, plus cascading?
        def delete_build_event(build_event: BuildEvent):
            nonlocal actions_to_run

            build_events_to_remove: List[BuildEvent] = [build_event]

            while len(build_events_to_remove) > 0:
                build_event_to_remove = build_events_to_remove.pop()
                try:
                    build_event_to_remove_index = self.build_events.index(build_event_to_remove)
                except ValueError:
                    # We are trying to remove a build event that does not exist
                    # This might be because we added the event twice because
                    # it had more than one input file that was deleted.
                    continue

                # Remove build event
                self.build_events[build_event_to_remove_index] = None

                # Find all the other build events to delete and add them to the list
                for cascading_build_event in self.build_events:
                    if cascading_build_event is None:
                        continue
                    for file in cascading_build_event.input_files:
                        if file in build_event_to_remove.output_files:
                            build_events_to_remove.append(cascading_build_event)

                # Delete all actions with inputs of the deleted files
                for action_to_run in actions_to_run:
                    for action_input_file in action_to_run.files():
                        if action_input_file in build_event_to_remove.output_files:
                            actions_to_run.delete(action_to_run.weak_hash())

                # Rebuild actions that can still exist without the deleted files
                rebuilt_actions = self.get_actions_with_from_quasifiles(build_event_to_remove.output_files)

                for rebuilt_action in rebuilt_actions:
                    actions_to_run.push(rebuilt_action)

                # Remove files that were built by the build events
                for output_file in build_event_to_remove.output_files:
                    _delete_file(output_file)
                self._remove_files_from_database(build_event_to_remove.output_files)


        def update_actions(files: List[str]) -> None:
            nonlocal actions_to_run
            nonlocal init

            self._add_files_to_database(files)
            new_actions = self._query_for_actions_from_files(files)
            for action in new_actions:
                actions_to_run.push(action)

            if init:

                for build_event in self.build_events:
                    if build_event is None:
                        continue

                    action = actions_to_run.get(build_event.weak_hash())

                    # No Link
                    if action is None:
                        delete_build_event(build_event)
                        continue # TODO: This should delete files and retrigger any actions with deleted files

                    # Strong Link, Exact same input files
                    elif set(action.files()) == set(build_event.input_files):
                        oldest_output = get_oldest_modified_time(build_event.output_files)
                        newest_input = get_newest_modified_time(build_event.input_files)

                        # Newer Outputs
                        if oldest_output > newest_input:
                            actions_to_run.delete(build_event.weak_hash())
                        # Newer Inputs
                        else:
                            delete_build_event(build_event)
                            continue # TODO: This should delete files and retrigger any actions with deleted files
                    # Weak Link, same groups and would trigger action deduplication, but different input files
                    else:
                        delete_build_event(build_event)
                        continue # TODO: This should delete files and retrigger any actions with deleted files

                self.build_events = [x for x in self.build_events if x is not None]

                # Do the things we need to do with the build log
                init = False
            else:
                for action in new_actions:
                    # TODO: We can probably optimize this lookup
                    for build_event in self.build_events:
                        if build_event is None:
                            continue

                        if action.weak_hash() == build_event.weak_hash():
                            delete_build_event(build_event)
                            break
                    
                self.build_events = [x for x in self.build_events if x is not None]

        update_actions(files)

        # Process each creator until there are none left
        while len(actions_to_run) > 0:
            action: Action = actions_to_run.pop()

            input_files = list(action.files())

            print()
            print(action.producer(self.producer_list).name)

            if len(input_files) > 5:
                print(fg_gray("  " + input_files[0]))
                print(fg_gray("  " + input_files[1]))
                print(fg_gray("  " + input_files[2]))
                print(fg_gray("  " + input_files[3]))
                print(fg_gray("  ...and {} other files".format(len(input_files)-4)))
            else:
                for i, file in enumerate(input_files):
                    print(fg_gray("  " + file))

            start = time.time()
            output_files: List[str] = action.producer(self.producer_list).function(action.input_files, action.match_groups)
            self.build_events.append(BuildEvent(
                producer_name=action.producer(self.producer_list).name,
                input_files=list(action.files()),
                output_files=output_files,
                match_groups=action.match_groups,
            ))

            duration = time.time() - start

            print(fg_gray("  │"))

            for i, file in enumerate(output_files):
                pipe_character = "├"
                if (i == len(output_files)-1):
                    pipe_character = "└"
                print(fg_gray("  {pipe_character}── {file}".format(
                    pipe_character=pipe_character,
                    file=file,
                )))

            print(fg_gray("  Completed in {:.2f}s".format(duration)))
            update_actions(output_files)

        # TODO: This is probably the wrong place to call this function. It
        # works, but when we begin testing for crashing actions we will find
        # that we want to save this much more often. Maybe at the end of
        # update_actions() or after calling action.producer().function() once
        # the new build log is added as a result of that function call.
        self.save_build_events()

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




    def _remove_files_from_database(self, files: List[str]) -> None:

        # Delete all files to delete in the database
        for producer_index, producer in enumerate(self.producer_list):
            for path in files:
                for field_name, pattern in producer.regex_field_patterns().items():
                    match: Optional[re.Match[str]] = re.match(pattern, path)

                    if match is None:
                        continue

                    self.remove_file_from_database(self.filecache, producer_index, field_name, path)

        pass



    ############################################################################
    ############################################################################
    # SQL LOGIC
    ############################################################################
    ############################################################################


    ############################################################################
    # get_field_table_name
    #
    # A helper function to produce the name of the table that stores matches
    # for a particular field.
    # TODO: The SQL logic should somehow be moved to scheduler.py
    ############################################################################
    @staticmethod
    def get_field_table_name(producer_index: int, field_id: str) -> str:
        return "producer{producer_index}_field{field_id}_matches".format(
            producer_index=producer_index,
            field_id=field_id
        )

    @staticmethod
    def get_match_group_column_name(producer: GenericProducer, group_name: str) -> str:
        return "group_{group_id}".format(
            group_id=producer.get_match_group_id(group_name)
        )

    ############################################################################
    # init_producer_cache
    #
    # Create the cache database for storing all the files that match a producer
    # field, and then initialize all of the tables in the database.
    # TODO: Logic from producers using sql commands should be moved to this
    # file instead.
    ############################################################################
    def init_producer_cache(self, producer_list: List[GenericProducer]) -> sqlite3.Connection:
        db = sqlite3.connect(':memory:')

        for producer_index, producer in enumerate(producer_list):
            for init_query in self.init_table_query(producer_index):
                with db:
                    db.execute(init_query)

        return db

    ############################################################################
    # init_table_query
    #
    # Create a series of sql query strings that are used to create all of the
    # tables for each field in this producer.
    ############################################################################
    def init_table_query(self, producer_index: int) -> List[str]:
        producer: GenericProducer = self.producer_list[producer_index]

        query_strings: List[str] = []

        for field_name in producer.regex_field_patterns():

            field_id: str = producer.get_field_id(field_name)

            field_table_name = Scheduler.get_field_table_name(
                producer_index=producer_index,
                field_id=field_id
            )

            table_columns: List[str] = [
                "filename TEXT UNIQUE",
                "is_updated INTEGER",
            ]

            for group_name in producer.get_match_groups(field_name):

                table_columns.append(Scheduler.get_match_group_column_name(
                    producer=producer,
                    group_name=group_name,
                )+" TEXT")

            query_string = "CREATE TABLE {field_table_name} ({table_columns});".format(
                field_table_name=field_table_name,
                table_columns=", ".join(table_columns)
            )

            query_strings.append(query_string)

        return query_strings

    ############################################################################
    # insert
    #
    # Insert a file that has matched a field for this producer into the
    # database table for that field.
    ############################################################################
    def insert_new_file(
        self,
        db: sqlite3.Connection,
        producer_index: int,
        field_name: str,
        filename: str,
        groups: Dict[str, str]
    ) -> None:
        
        query_string, binds = self.insert_new_file_querystring(
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

    def insert_new_file_querystring(
        self,
        producer_index: int,
        field_name: str,
        filename: str,
        groups: Dict[str, str]
    ) -> Tuple[str, List[str]]:
        producer = self.producer_list[producer_index]
        field_id = producer.get_field_id(field_name)
        table_name = Scheduler.get_field_table_name(producer_index=producer_index, field_id=field_id)

        fields = ["filename", "is_updated"] + [Scheduler.get_match_group_column_name(producer=producer, group_name=group_name) for group_name in groups.keys()]

        binds = [filename, 1] + list(groups.values())

        # query_string: str = "INSERT INTO {table} ({fields}) VALUES ({value_binds}) ON CONFLICT(filename) DO UPDATE SET is_updated=1".format(
        query_string: str = "INSERT INTO {table} ({fields}) VALUES ({value_binds})".format(
            table=table_name,
            fields=", ".join(fields),
            value_binds=", ".join("?" * len(fields))
        )

        return query_string, binds

    def remove_file_from_database(
        self,
        db: sqlite3.Connection,
        producer_index: int,
        field_name: str,
        filename: str,
    ) -> None:

        query_string = self.remove_file_from_database_sql(producer_index, field_name)
        with db:
            db.execute(
                query_string,
                {
                    "filename": filename
                },
            )

    def remove_file_from_database_sql(
        self,
        producer_index: int,
        field_name: str,
    ) -> str:

        producer = self.producer_list[producer_index]
        table_name = Scheduler.get_field_table_name(
            producer_index=producer_index,
            field_id= producer.get_field_id(field_name)
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
    # def query_filesets(self, db: sqlite3.Connection, producer_index: int) -> List[Tuple[InputFileDatatype, Dict[str, str]]]:
    def query_filesets(
        self,
        db: sqlite3.Connection,
        producer_index: int
    ) -> List[Tuple[Any, Dict[str, str]]]:
        query_string = self.new_filesets_querystring(producer_index)

        producer = self.producer_list[producer_index]

        # output_data: List[Tuple[InputFileDatatype, Dict[str, str]]] = []
        output_data: List[Tuple[Any, Dict[str, str]]] = []
        with db:
            cur = db.execute(
                query_string,
            )

            columns = [ x[0] for x in cur.description ]
            columns_lookup = { value: index for index, value in enumerate(columns) }
            # print(columns_lookup)

            for row in cur.fetchall():

                new_element = {}
                groups: Dict[str, str] = {}

                for new_element_field_name, pattern in producer.input_path_patterns_dict().items():
                    new_element_field_id = producer.get_field_id(new_element_field_name)
                    if pattern == "":
                        new_element[new_element_field_name] = ""
                        continue
                    elif pattern == []:
                        new_element[new_element_field_name] = []
                        continue

                    value: str = row[columns_lookup["field_"+new_element_field_id]]
                    if isinstance(pattern, str):
                        new_element[new_element_field_name] = value
                    elif isinstance(pattern, list):
                        new_element[new_element_field_name] = sorted(parse_comma_escape(value))
                    else:
                        raise TypeError()

                for group_name in producer.get_all_match_groups():
                    group_id = producer.get_match_group_id(group_name)
                    groups[group_name] = row[columns_lookup["group_"+group_id]]


                # If at least one file is updated then this creator should be
                # constructed.
                is_updated = row[columns_lookup["is_updated"]]
                if is_updated > 0:
                    output_data.append((new_element, groups))

        return output_data


    def new_filesets_querystring(self, producer_index: int) -> str:

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


        update_tracking_columns: List[str] = []

        # mypy complains about iterating over a typeddict even though it is a dict
        for field_name, field in producer.input_path_patterns_dict().items():
            if field == "":
                continue
            elif field == []:
                continue

            field_id = producer.get_field_id(field_name)

            table_name = Scheduler.get_field_table_name(
                producer_index=producer_index,
                field_id=field_id
            )

            table_contents = table_name

            field_alias="\"field_{field_id}\"".format(
                field_id=field_id,
            )

            if isinstance(field, str):
                columns.append("{table_name}.filename AS {field_alias}".format(
                    table_name=table_name,
                    field_alias=field_alias,
                ))
                group_by_columns.append(str(len(columns)))


            # If the field is a list then we want to grab each file and put it into a list
            # this is done by using
            elif isinstance(field, list):


                match_columns = [Scheduler.get_match_group_column_name(producer, match_group) for match_group in producer.get_match_groups(field_name)]
                new_table_name = table_name + "_mod"

                table_contents = "(SELECT GROUP_CONCAT(REPLACE(REPLACE(filename, '\\','\\\\'), ',', '\\,'), ',') as filename, {match_columns}, SUM(is_updated) as is_updated FROM {table_name} GROUP BY {match_columns}) as {new_table_name}".format(
                    table_name=table_name,
                    new_table_name=new_table_name,
                    match_columns=",".join(match_columns)
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

            # Add the is_updated column from this table to the list of columns
            # to sum as a check if any of the files inside are updated.
            update_tracking_columns.append("{table_name}.is_updated".format(
                table_name=table_name
            ))


        field_joins: List[str] = []
        for match_group_name, group_tables in field_groups.items():
            first_table = group_tables[0]

            columns.append("{first_table}.{group_column_name}".format(
                first_table=first_table,
                group_column_name=Scheduler.get_match_group_column_name(producer, match_group_name)
            ))
            group_by_columns.append(str(len(columns)))

            for table in group_tables[1:]:
                field_joins.append("{first_table}.{group_column_name} = {table}.{group_column_name}".format(
                    first_table=first_table,
                    group_column_name=Scheduler.get_match_group_column_name(producer, match_group_name),
                    table=table,
                ))

        # Prevent the WHERE clause from being blank ever.
        # TODO: The WERE clause should probably just be removed entirely but the
        # query is already imperfect by not using JOINs instead so this will be
        # left until we re-evaluate the query again.
        if len(field_joins) == 0:
            field_joins = ["1=1"]


        columns.append(
            "SUM({}) AS \"is_updated\"".format(
                "+".join(update_tracking_columns)
            )
        )

        query_string = "SELECT {columns} FROM {field_tables} WHERE {field_wheres} GROUP BY {group_by_columns};".format(
            columns=", ".join(columns),
            field_tables=", ".join(tables),
            field_wheres=" AND ".join(field_wheres + field_joins),
            group_by_columns=", ".join(group_by_columns)
        )

        return query_string


    def mark_all_files_old(self, db: sqlite3.Connection) -> None:
        for mark_files_query in self.mark_all_files_old_querystrings():
            with db:
                db.execute(mark_files_query)

    def mark_all_files_old_querystrings(self) -> List[str]:

        query_strings = []
        for producer_index, producer in enumerate(self.producer_list):
            for field_name, field in producer.input_path_patterns_dict().items():
                if field == "":
                    continue
                elif field == []:
                    continue

                field_id = producer.get_field_id(field_name)

                table_name = Scheduler.get_field_table_name(
                    producer_index=producer_index,
                    field_id=field_id
                )

                query_strings.append("UPDATE {table_name} SET is_updated = 0 WHERE is_updated != 0;".format(
                    table_name=table_name
                ))

        return query_strings



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
# make_required_directories
#
# Takes in a list of files and then creates all of the directories needed in
# order for those files to be written to if they do not already exist.
################################################################################
def make_required_directories(files: List[str]) -> None:
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
    # recursion by just appending the values.
    paths = list(paths)
    time_list: List[float] = []
    for path in paths:
        # TODO: Decide if we want to re-add this recursive functionality. If so
        #       then it needs some method of testing.
        # if (os.path.isdir(path)):
        #     for subpath in os.listdir(path):
        #         paths.append(os.path.join(path, subpath))
        #     continue

        time = _check_file_modification_time(path)
        if time is None:
            time = default

        time_list.append(time)

    # Sanity check that there are timestamps in the list before passing them
    # to the aggregator.
    if len(time_list) == 0:
        return default

    return aggregator(time_list)


# A function that looks up the modification time of a file. Returns None if the file does not exist.
def _check_file_modification_time(path: str) -> Optional[float]:
    if not os.path.exists(path):
        return None

    # If a path is a directory add all its children to the paths list
    if (os.path.isdir(path)):
        raise ValueError
    else:
        return os.path.getmtime(path)

def _delete_file(path: str) -> None:
    if os.path.exists(path):
        os.unlink(path)


################################################################################
# parse_comma_escape
#
# Parses the escaped comma string returned from the SQL query back into an
# array. The query escapes all backslashes and commas, then uses a comma to
# delimite each element in the array.
# TODO: The SQL logic should somehow be moved to scheduler.py
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
