from typing import List, TypedDict, Dict
import os
import shutil
import json
import re

from pylib.filehash import getfilehash
from .producer import Producer, GenericProducer
from .scheduler import Scheduler


# Convenience Class for anything with a single input or output file
class SingleFile(TypedDict):
    file: str


# Convenience Class for anything with a single group of input or output files
class MultiFile(TypedDict):
    files: List[str]



################################################################################
# copy_file
#
# Create a producer to copy a file from one location to another location
# without any changes.
################################################################################
def copy_file(
    name: str,
    target_file: str,
    destination_file: str,
) -> Producer[SingleFile]:
    def function(input_files: SingleFile, groups: Dict[str, str]) -> List[str]:
        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
        shutil.copyfile(target_file, destination_file)
        return [destination_file]

    return Producer(
        name=name,
        input_path_patterns={
            "file": "^" + re.escape(target_file) + "$",
        },
        function=function
    )


################################################################################
# copy_file_with_hash
# 
# Create a producer to copy a file to another location adding the hash of the
# file to the filename based on the output_file_template formatstring. Also
# saves a metadata file which contains the hashed file's filename.
#
# TODO: Think about changing the output and metedata args to be less complex.
################################################################################
def copy_file_with_hash(
    name: str,
    input_file_pattern: str,
    output_file_template: str = "output/{filename}-{filehash}{extension}",
    metadata_file_template: str = "cache/{filename}{extension}.json",
) -> Producer[SingleFile]:
    ############################################################################
    # function
    #
    # The internal producer function used inside of the copy_file_with_hash
    # generated producer. Performce the actual hash and copy operations.
    ############################################################################
    def function(input_files: SingleFile, groups: Dict[str, str]) -> List[str]:
        input_file: str = input_files["file"]
        filehash = getfilehash(input_file)
        filename = os.path.splitext(os.path.basename(input_file))[0]
        extension = os.path.splitext(os.path.basename(input_file))[1]

        output_file: str = output_file_template.format(
            filename=filename,
            filehash=filehash,
            extension=extension,
            **groups
        )

        metadata_file: str = metadata_file_template.format(
            filename=filename,
            filehash=filehash,
            extension=extension,
            **groups
        )

        # Copy the file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        shutil.copyfile(input_file, output_file)

        # Write the hashed file name to a known location
        os.makedirs(os.path.dirname(metadata_file), exist_ok=True)
        with open(metadata_file, 'w') as f:
            json.dump({
                "filename": output_file
            }, f)

        return [
            output_file,
            metadata_file
        ]

    producer: Producer[SingleFile] = Producer(
        name=name,
        input_path_patterns={
            "file": input_file_pattern,
        },
        function=function,
    )

    return producer


################################################################################
#
################################################################################
def filename_from_metadatafile(metadata_file: str, rel: str = "") -> str:
    with open(metadata_file) as f:
        if rel == "":
            return json.load(f)["filename"]
        else:
            return os.path.relpath(json.load(f)["filename"], rel)

__all__ = [
    "Producer",
    "GenericProducer",
    "Scheduler",
]
