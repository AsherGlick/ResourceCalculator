from typing import List, Tuple, Dict
import os
import shutil
import subprocess

from pylib.producer import Producer, SingleFile


################################################################################
# uglify_copyfile
#
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
# uglify_js_string
#
# Uglify js String calls and uglification / minification process on a single
# string, which is then returned.
# TODO: This methodology does not support the Producer model and should be
# revisited.
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
# uglify_js_producer
#
# Creates a producer that minifies a javascript file.
################################################################################
def uglify_js_producer(input_file: str, output_file: str, categories: List[str]) -> Producer[SingleFile, SingleFile]:
    return Producer(
        input_path_patterns={
            "file": "^" + input_file + "$",
        },
        paths=uglify_paths,
        function=uglify_copyfile,
        categories=categories + ["minifyjs"]
    )


################################################################################
# uglify_paths
#
# The input output path generation function for the the uglify_js producer.
################################################################################
def uglify_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    return (
        input_files,
        {
            "file": os.path.join("output", os.path.basename(input_files["file"]))
        })
