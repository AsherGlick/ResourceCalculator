import shutil
import subprocess
from pylib.producers import Producer
from typing import List
import re

_skip_uglify = False


################################################################################
# Helper function to flip the skip uglify flag that will bypass this module
################################################################################
def set_skip_uglify_flag() -> None:
    global _skip_uglify
    _skip_uglify = True


################################################################################
# Uglify Copyfile calls an uglification process on an entire file and writes
# the output to a new file.
################################################################################
def uglify_copyfile(in_file: str, match: re.Match, out_files: List[str]) -> None:
    if len(out_files) != 1:
        raise ValueError("Must copy " +in_file+" to only one location not" + str(out_files))

    out_file = out_files[0]

    if _skip_uglify:
        shutil.copyfile(in_file, out_file)
        return

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
    if _skip_uglify:
        return js_string

    try:
        result = subprocess.run(["./node_modules/.bin/terser", "--mangle", "--compress"], input=js_string.encode("utf-8"), stdout=subprocess.PIPE)
        return result.stdout.decode("utf-8")
    except Exception as e:
        print("WARNING: Javascript compression failed")
        print("        ", e)
    return js_string


def uglify_js_producer(input_file: str, output_file: str, categories: List[str]) -> Producer:
    return Producer(
        input_path_patterns=["^"+input_file+"$"],
        output_paths=Producer.static_output(output_file),
        function=uglify_copyfile,
        categories=categories
    )