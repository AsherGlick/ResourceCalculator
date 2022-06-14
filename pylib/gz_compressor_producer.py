import shutil
import subprocess
from pylib.producers import Producer, SingleFile
from typing import List, Dict, Tuple
import re
import os
import math
import json
from PIL import Image  # type: ignore
import gzip


def gz_compressor_producers() -> List[Producer]:
    return [
        Producer(
            input_path_patterns=[r"^output/.*\.(?:html|js|css)$"],
            paths=gz_compress_paths,
            function=gz_compress_function,
            categories=gz_categories
        ),
    ]

def gz_categories(input_files: SingleFile) -> List[str]:
    return ["compress", "gz"]

def gz_compress_paths(index: int, regex: str, match: re.Match) -> Tuple[SingleFile, SingleFile]:
    path = match.group(0)
    return (
        {
            "file": path
        },{
            "file": path + ".gz"
        }
    )

# ################################################################################
# # pre_compress_output_files
# #
# # Walks through the output directory and compresses any file with a .html, .css
# # or .js extension with gz so that Apache can serve its compressed state
# # automatically.
# ################################################################################
def gz_compress_function(input_files: SingleFile, output_files: SingleFile) -> None:
    output_file = output_files["file"]
    input_file = input_files["file"]

    with open(input_file, 'rb') as infile, gzip.open(output_file, 'wb') as outfile:
        shutil.copyfileobj(infile, outfile)
