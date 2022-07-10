from pylib.producer import Producer, SingleFile, producer_copyfile, GenericProducer
from typing import List, Tuple, Dict
import os


################################################################################
# plugins_producers
#
# Creates the producers for copying plugin files from their source directories
# to the output directories.
################################################################################
def plugins_producers(calculator_dir_regex: str) -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                # TODO: Get rid of the full path capture group when the bug of
                # these files deduplicating themselves on only "calculator_dir"
                # is fixed.
                "file": r"^(?P<fullpath>resource_lists/(?P<calculator_dir>{calculator_dir_regex})/plugins/.+/.+)$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
            },
            paths=plugins_paths,
            function=producer_copyfile,
            categories=["plugins"]
        )
    ]


################################################################################
# plugin_paths
#
# The input and output paths generation function for copying plugin files from
# thier source directories to the output directories.
################################################################################
def plugins_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    return (
        input_files,
        {
            "file": os.path.join("output", os.path.relpath(input_files["file"], "resource_lists")),
        }
    )
