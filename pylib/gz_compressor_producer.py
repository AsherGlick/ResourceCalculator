from typing import List, Dict, Tuple
import gzip
import shutil

from pylib.producer import Producer, SingleFile, GenericProducer

################################################################################
# gz_compressor_rpoducer
#
# Creates producers for generating the `.gz` compressed files for any output
# html, js, css file.
################################################################################
def gz_compressor_producers() -> List[GenericProducer]:
    return [
        Producer(
            name="Compress HTTP Files",
            input_path_patterns={
                "file": r"^output/.*\.(?:html|js|css)$"
            },
            function=gz_compress_function,
        ),
    ]


################################################################################
# gz_compress_function
#
# Takes the input file and gz compresses it into the output file without
# deleting the original.
################################################################################
def gz_compress_function(input_files: SingleFile, groups: Dict[str, str]) -> List[str]:
    input_file = input_files["file"]
    output_file = input_file + ".gz"

    with open(input_file, 'rb') as infile, gzip.open(output_file, 'wb') as outfile:
        shutil.copyfileobj(infile, outfile)

    return [output_file]
