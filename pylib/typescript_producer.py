from typing import List, Tuple, TypedDict, Dict
import json
import os
import subprocess

from pylib.producer import Producer, MultiFile


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
    categories: List[str]
) -> Producer[TypescriptInputFiles, MultiFile]:
    return Producer(
        input_path_patterns={
            "inputs": [],
            "tsconfig_file": "^" + ts_project_config + "$",
        },
        paths=typescript_resource_paths,
        function=build_typescript,
        categories=categories + ["typescript"]
    )


################################################################################
# typescript_resource_paths
#
# The input and output paths generation function for creating compiled
# typescript files. Uses the configuration file to determine what the input and
# output files will be.
################################################################################
def typescript_resource_paths(input_files: TypescriptInputFiles, groups: Dict[str, str]) -> Tuple[TypescriptInputFiles, MultiFile]:
    tsconfig_path = input_files["tsconfig_file"]
    input_folder = os.path.dirname(tsconfig_path)

    # Get the list of files and the typescript output directory
    with open(tsconfig_path) as f:
        tsconfig = json.load(f)

    files: List[str] = tsconfig["files"]
    output_directory: str = tsconfig["compilerOptions"]["outDir"]

    output_paths = []
    input_paths = []

    for file in files:

        output_path = os.path.normpath(os.path.join(input_folder, output_directory, file))

        if output_path.endswith(".ts"):
            output_path = output_path[:-3] + ".js"
        else:
            raise ValueError("Expected only typescript files as input")

        input_path = os.path.join(input_folder, file)

        output_paths.append(output_path)
        input_paths.append(input_path)

    return (
        {
            "inputs": input_paths,
            "tsconfig_file": tsconfig_path
        }, {
            "files": output_paths
        }
    )


################################################################################
# build_typescript
#
# Call the typescript compiler tsc to generate compiled typescript for the
# files in the typescript project.
################################################################################
def build_typescript(input_files: TypescriptInputFiles, output_files: MultiFile) -> None:
    tsconfig_file = input_files["tsconfig_file"]

    typescript_folder = os.path.dirname(tsconfig_file)
    subprocess.run(["node_modules/.bin/tsc", "--project", typescript_folder])
