import shutil
import subprocess
from pylib.producer import Producer, SingleFile
from typing import List, Callable, Tuple, Dict
import re
import os


################################################################################
# Uglify Copyfile calls an uglification process on an entire file and writes
# the output to a new file.
################################################################################
def uglify_copyfile(input_files: SingleFile, output_files: SingleFile) -> None:
    in_file: str = input_files["file"]
    out_file: str = output_files["file"]

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
def uglify_js_producer(input_file: str, output_file: str, categories: List[str]) -> Producer[SingleFile, SingleFile]:
    return Producer(
        input_path_patterns={
            "file": "^"+input_file+"$",
        },
        paths=uglify_paths,
        function=uglify_copyfile,
        categories= categories + ["minifyjs"]
    )


################################################################################
#
################################################################################
def uglify_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    return (
        input_files,
        {
            "file": os.path.join("output", os.path.basename(input_files["file"]))
        })
