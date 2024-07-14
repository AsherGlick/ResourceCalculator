from typing import List, TypedDict, Dict
import os
import subprocess
import re

from pylib.producer import Producer


################################################################################
# TypescriptInputFiles
#
# A TypedDict representing the input files structure for the producer that
# creates compiled javascript from typescript.
################################################################################
class TypescriptInputFiles(TypedDict):
    inputs: List[str]
    tsconfig_file: str


################################################################################
# typescript_producer
#
# Build the producers list for compiling typescript to javascript given a
# particular tsconfig.json file.
################################################################################
def typescript_producer(
    ts_project_config: str,
) -> List[Producer[TypescriptInputFiles]]:
    ts_project_dir = os.path.dirname(ts_project_config)

    result = subprocess.run(
        ["node_modules/.bin/tsc", "--project", ts_project_dir, "--listFilesOnly"],
        capture_output=True,
        text=True
    )
    
    # TODO: This list is only built once when the producer is defined. Any new
    #   files would not be added here. This shoudld either become the standard
    #   pattern or upgrade to allow for live changes through some mechanism.
    input_files = []
    for line in result.stdout.split("\n"):
        if line == "":
            continue
        relative_path = os.path.relpath(line)
        regex_path = "^" + re.escape(relative_path) + "$"
        input_files.append(regex_path)
    input_files_regex = "|".join(input_files)

    return [
        Producer(
            name="Compile Typescript to Javascript",
            input_path_patterns={
                "inputs": [input_files_regex],
                "tsconfig_file": "^" + re.escape(ts_project_config) + "$",
            },
            function=build_typescript,
        )
    ]


################################################################################
# build_typescript
#
# Call the typescript compiler tsc to generate compiled typescript for the
# files in the typescript project.
################################################################################
def build_typescript(input_files: TypescriptInputFiles, groups: Dict[str, str]) -> List[str]:
    tsconfig_file = input_files["tsconfig_file"]

    # Run tsc on the typescript code
    typescript_folder = os.path.dirname(tsconfig_file)
    result = subprocess.run(
        ["node_modules/.bin/tsc", "--project", typescript_folder, "--listEmittedFiles"],
        capture_output=True,
        text=True,
    )

    output_files = []
    for line in result.stdout.split("\n"):
        if line == "":
            continue
        line = line.removeprefix("TSFILE: ")
        relative_path = os.path.relpath(line)
        output_files.append(relative_path)

    return output_files
