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
            input_path_patterns={
                "file": r"^output/.*\.(?:html|js|css)$"
            },
            paths=gz_compress_paths,
            function=gz_compress_function,
            categories=["compress", "gz"]
        ),
    ]


################################################################################
# gz_compress_paths
#
# The input and output paths generation function for compressing specific files
# into the output directory.
################################################################################
def gz_compress_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    path = input_files["file"]
    return (
        input_files,
        {
            "file": path + ".gz"
        }
    )


################################################################################
# gz_compress_function
#
# Takes the input file and gz compresses it into the output file without
# deleting the original.
################################################################################
def gz_compress_function(input_files: SingleFile, output_files: SingleFile) -> None:
    output_file = output_files["file"]
    input_file = input_files["file"]

    with open(input_file, 'rb') as infile, gzip.open(output_file, 'wb') as outfile:
        shutil.copyfileobj(infile, outfile)
