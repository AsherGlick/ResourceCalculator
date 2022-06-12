from pylib.producers import Producer
import json
import os
import subprocess
from typing import List
import re


################################################################################
# typescript_producer
#
# Build the producers list for compiling typescript to javascript given a
# particular tsconfig.json file.
################################################################################
def typescript_producer(typescript_directory: str, categories: List[str]) -> List[Producer]:

    input_directory_pattern = "^" + typescript_directory + "$"

    return [Producer(
        input_path_patterns=[input_directory_pattern],
        output_paths=output_files,
        function=build_typescript,
        categories=categories
    )]


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
def build_typescript(folder: str, match: re.Match, output_files: List[str]) -> None:
    subprocess.run(["node_modules/.bin/tsc", "--project", folder])