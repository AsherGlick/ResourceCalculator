from typing import List, TypedDict
import shutil
from .producer import Producer
from .scheduler import Scheduler


# Convenience Class for anything with a single input or output file
class SingleFile(TypedDict):
    file: str

# Convenience Class for anything with a single group of input or output files
class MultiFile(TypedDict):
    files: List[str]

# Convenience function for situations where all that needs to be done is to
# copy a single input to a single output
def producer_copyfile(input_files: SingleFile, output_files: SingleFile) -> None:
    input_file: str = input_files["file"]
    output_file: str = output_files["file"]

    # Copy the file
    shutil.copyfile(input_file, output_file)

