from pylib.producer import Producer, SingleFile, GenericProducer
from typing import List, Dict
import os
import shutil


################################################################################
# plugins_producers
#
# Creates the producers for copying plugin files from their source directories
# to the output directories.
################################################################################
def plugins_producers(calculator_dir_regex: str) -> List[GenericProducer]:

    def function(input_files: SingleFile, groups: Dict[str, str]) -> List[str]:
        target_file=input_files["file"]
        destination_file = os.path.join("output", os.path.relpath(input_files["file"], "resource_lists"))

        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
        shutil.copyfile(target_file, destination_file)
        return [destination_file]

    return [
        Producer(
            name="Copy Plugin Directories",
            input_path_patterns={
                # TODO: Get rid of the full path capture group when the bug of
                # these files deduplicating themselves on only "calculator_dir"
                # is fixed.
                "file": r"^(?P<fullpath>resource_lists/(?P<calculator_dir>{calculator_dir_regex})/plugins/.+/.+)$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
            },
            function=function,
        )
    ]
