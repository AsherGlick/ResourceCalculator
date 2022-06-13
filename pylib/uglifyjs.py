import shutil
import subprocess
from pylib.producers import Producer, InputFileDatatype, OutputFileDatatype
from typing import List, Callable, Tuple
import re
import os


################################################################################
# Uglify Copyfile calls an uglification process on an entire file and writes
# the output to a new file.
################################################################################
def uglify_copyfile(input_files: InputFileDatatype, output_files: OutputFileDatatype) -> None:
    in_file: str = input_files["input"]
    out_file: str = output_files["output"]

    try:
        subprocess.run(["./node_modules/.bin/terser", "--mangle", "--compress", "-o", out_file, in_file])
    except Exception as e:
        print("WARNING: Javascript compression failed")
        print("        ", e)
        print("        Falling back to regular copy")
        shutil.copyfile(in_file, out_file)


################################################################################
# Uglify js String calls and uglification / minification process on a single
# string, which is then returned.
################################################################################
def uglify_js_string(js_string: str) -> str:
    try:
        result = subprocess.run(["./node_modules/.bin/terser", "--mangle", "--compress"], input=js_string.encode("utf-8"), stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8")
    except Exception as e:
        print("WARNING: Javascript compression failed")
        print("        ", e)
    return js_string


################################################################################
#
################################################################################
def uglify_js_producer(input_file: str, output_file: str, categories: List[str]) -> Producer:
    return Producer(
        input_path_patterns=["^"+input_file+"$"],
        paths=uglify_paths,
        function=uglify_copyfile,
        categories=uglify_categories(categories)
    )


################################################################################
#
################################################################################
def uglify_categories(parent_categories: List[str]) -> Callable[[InputFileDatatype], List[str]]:
    def category_list(input_files: InputFileDatatype) -> List[str]:
        # flat_input_paths: List[str] = input_files["inputs"]

        categories = []
        categories += parent_categories
        categories.append("minifyjs")
        # categories += flat_input_paths

        return categories
    return category_list


################################################################################
#
################################################################################
def uglify_paths(index: int, regex: str, match: re.Match) -> Tuple[InputFileDatatype, OutputFileDatatype]:
    return ({
            "input": match.group(0)
        },{
            "output": os.path.join("output", os.path.basename(match.group(0)))
        })
