from typing import Callable, List, TypedDict, Dict, Tuple
import os
import shutil
import json

from pylib.filehash import getfilehash
from .producer import Producer, GenericProducer
from .scheduler import Scheduler


# Convenience Class for anything with a single input or output file
class SingleFile(TypedDict):
    file: str


# Convenience Class for anything with a single group of input or output files
class MultiFile(TypedDict):
    files: List[str]



# Convenience function for situations where all that needs to be done is to
# copy a single input to a single output
def producer_copyfile(input_files: SingleFile, output_files: SingleFile) -> None:
    input_file: str = input_files["file"]
    output_file: str = output_files["file"]

    # Copy the file
    shutil.copyfile(input_file, output_file)


def single_file_static_output_path(output_file: str) -> Callable[[SingleFile, Dict[str,str]], Tuple[SingleFile, SingleFile]]:
    def path_passthrough(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
        return(
            input_files,
            {
                "file": output_file
            }
        )
    return path_passthrough



################################################################################
# TODO: I think this pattern is not a good one and we are only forced to use it
# because there is not a spec out for how files should be delted when they are
# no longer needed. If we had that then we could just write a regex that matches
# onto the generated file itself and uses that as an input as to where it is.
# but without the ability to delete files, if we have two instances of the same
# ish file with different file hashes then we will pick both of them up as
# input files and that might cause havoc. So this is a temporary workaround
# until we have better functionality in omnibuild.
################################################################################

################################################################################
# SingleFileWithHash
#
# A helper datastructure for storing a single filepath, and another filepath
# that contians metadata information. This is done so that the single filepath
# can be more dynamic, and the single filepath can contain a pointer to where
# the more dynamic filepath lives.
#
# TODO: Delete this class, see note above
################################################################################
class SingleFileWithHash(TypedDict):
    file: str
    hash_metadata_file: str

# TODO: Delete this function, see note above
def paths_for_copy_file_with_hash(
    output_file_template: str,
    cache_file_template: str
) -> Callable[[SingleFile, Dict[str, str]], Tuple[SingleFile, SingleFileWithHash]]:
    def output_file_copyfile_with_hash(
        input_files: SingleFile,
        groups: Dict[str, str]
    ) -> Tuple[SingleFile, SingleFileWithHash]:

        input_file = input_files["file"]
        filehash = getfilehash(input_file)
        filename = os.path.splitext(os.path.basename(input_file))[0]
        extension = os.path.splitext(os.path.basename(input_file))[1]

        output_file = output_file_template.format(
            filename=filename,
            filehash=filehash,
            extension=extension,
            **groups
        )

        metadata_file = cache_file_template.format(
            filename=filename,
            filehash=filehash,
            extension=extension,
            **groups
        )

        return (
            input_files,
            {
                "file": output_file,
                "hash_metadata_file": metadata_file,
            }
        )
    return output_file_copyfile_with_hash

################################################################################
# function_for_copy_file_with_hash
#
# Convenience function for situations where all that needs to be done is to
# copy a single input to a single output
#
# TODO: Delete this function, see note above
################################################################################
def function_for_copy_file_with_hash(input_files: SingleFile, output_files: SingleFileWithHash) -> None:
    input_file: str = input_files["file"]
    output_file: str = output_files["file"]
    output_metadata_file: str = output_files["hash_metadata_file"]

    # Copy the file
    shutil.copyfile(input_file, output_file)

    # Write the hashed file name to a known location
    with open(output_metadata_file, 'w') as f:
        json.dump({
            "filename": output_file
        }, f)


################################################################################
# copy_file_with_hash
# 
# This function copies and input file to an output file and a metadata file
# that contains information about the copied file. Format strings can be used
# to define the ouput files. In addition to all of the regex matchgroups there
# are three extra values that can be inlcuded in the format string.
#
# filename - The name of the file without an extention or directories
# hash - the hash of the contents of the file
# extension - the extention of the file
#
# TODO: Delete this function, see note above
################################################################################
def copy_file_with_hash(
    input_file_pattern: str,
    output_file_template: str = "output/{filename}-{filehash}{extension}",
    cache_file_template: str = "cache/{filename}{extension}.json",
    categories: List[str] = [],
) -> Producer[SingleFile, SingleFileWithHash]:
    producer: Producer[SingleFile, SingleFileWithHash] = Producer(
        input_path_patterns={
            "file": input_file_pattern,
        },
        paths=paths_for_copy_file_with_hash(output_file_template, cache_file_template),
        function=function_for_copy_file_with_hash,
        categories=categories
    )

    return producer

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
