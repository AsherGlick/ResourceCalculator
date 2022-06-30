from pylib.producer import Producer, MultiFile
import json
import os
import subprocess
from typing import List, Tuple, Callable, TypedDict, Dict
import re


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


    return ({
            "inputs": input_paths,
            "tsconfig_file": tsconfig_path
        },{
            "files": output_paths
        })
    
# def producer_copyfile(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:




def output_files(input_path: str, match: "re.Match[str]") -> List[str]:
    tsconfig_path = os.path.join(input_path, "tsconfig.json")

    # Get the list of files and the typescript output directory
    with open(tsconfig_path) as f:
        tsconfig = json.load(f)

    files: List[str] = tsconfig["files"]
    output_directory: str = tsconfig["compilerOptions"]["outDir"]


    output_paths = []

    for file in files:

        output_path = os.path.normpath(os.path.join(input_path, output_directory, file))

        if output_path.endswith(".ts"):
            output_path = output_path[:-3] + ".js"

        input_path = os.path.join(input_path, file)

        output_paths.append(output_path)

    return output_paths


################################################################################
# build_typescript
#
# Call the tsc 
################################################################################
def build_typescript(input_files: TypescriptInputFiles, output_files: MultiFile) -> None:
    tsconfig_file = input_files["tsconfig_file"]

    typescript_folder = os.path.dirname(tsconfig_file)
    subprocess.run(["node_modules/.bin/tsc", "--project", typescript_folder])
