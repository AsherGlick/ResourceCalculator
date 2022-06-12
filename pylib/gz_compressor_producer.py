import shutil
import subprocess
from pylib.producers import Producer
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
            output_paths=gz_compress_output_paths,
            function=gz_compress_function,
            categories=["compress", "gz"]
        ),
    ]

def gz_compress_output_paths(path: str, match: re.Match) -> List[str]:
    return [
        path + ".gz"
    ]

# ################################################################################
# # pre_compress_output_files
# #
# # Walks through the output directory and compresses any file with a .html, .css
# # or .js extension with gz so that Apache can serve its compressed state
# # automatically.
# ################################################################################
def gz_compress_function(input_file: str, match: re.Match, output_files: List[str]) -> None:
    if len(output_files) != 1:
        raise ValueError("Expected just one output file but got" + str(output_files))
    
    output_file = output_files[0]

    with open(input_file, 'rb') as infile, gzip.open(output_file, 'wb') as outfile:
        shutil.copyfileobj(infile, outfile)
