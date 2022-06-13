from pylib.producers import Producer, MultiFile
import json
import os
import subprocess
from typing import List, Tuple, Callable, TypedDict
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
def typescript_producer(ts_project_config: str, categories: List[str]) -> List[Producer]:

    input_directory_pattern = "^" + ts_project_config + "$"

    return [
        Producer(
            input_path_patterns=[input_directory_pattern],
            paths=typescript_resource_paths,
            function=build_typescript,
            categories=typescript_categories(categories)
        )
    ]

def typescript_categories(parent_categories: List[str]) -> Callable[[TypescriptInputFiles], List[str]]:
    def category_list(input_files: TypescriptInputFiles) -> List[str]:
        # flat_input_paths: List[str] = input_files["inputs"]

        categories = []
        categories += parent_categories
        categories.append("typescript")
        # categories += flat_input_paths

        return categories
    return category_list

def typescript_resource_paths(index: int, regex: str, match: re.Match) -> Tuple[TypescriptInputFiles, MultiFile]:
    tsconfig_path = match.group(0)
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




def output_files(input_path: str, match: re.Match) -> List[str]:
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
