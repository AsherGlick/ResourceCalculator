from pylib.producer import Producer, SingleFile, producer_copyfile, GenericProducer
from typing import List, Tuple, Dict
import os


################################################################################
# plugins_producers
#
# Creates the producers for copying plugin files from their source directories
# to the output directories.
################################################################################
def plugins_producers() -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                "file": r"^resource_lists/(?P<calculator_dir>[a-z ]+)/plugins/.+/.+$",
            },
            paths=plugins_paths,
            function=producer_copyfile,
            categories=["editor"]
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
