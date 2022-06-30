import shutil
import subprocess
from pylib.producer import Producer, MultiFile, SingleFile
from typing import List, Dict, Tuple, TypedDict
import re
import os
import math
import json
from PIL import Image  # type: ignore



class ImagePackOutputFiles(TypedDict):
    image_file: str
    image_layout_file: str

def item_image_producers() -> List[Producer]:
    return [
        # Pack Image
        Producer(
            input_path_patterns={
                "files": [r"^resource_lists/(?P<calculator_dir>[a-z ]+)/items/.*$"],
            },
            paths=image_pack_paths,
            function=image_pack_function,
            categories=["image"]
        ),

        # Compress Image
        Producer(
            input_path_patterns={
                "file": r"^cache/(?P<calculator_dir>[a-z ]+)/packed_image\.png$",
            },
            paths=image_compress_paths,
            function=image_compress_function,
            categories=["image", "compress", "imagecompress"]
        )
    ]


def image_pack_paths(input_files: MultiFile, categories: Dict[str,str]) -> Tuple[MultiFile, ImagePackOutputFiles]:
    calculator_page = categories["calculator_dir"]

    calculator_imagefile = os.path.join("cache", calculator_page, "packed_image.png")
    calculator_image_layout = os.path.join("cache", calculator_page, "packed_image_layout.json")

    return (
        input_files,
        {
            "image_file": calculator_imagefile,
            "image_layout_file": calculator_image_layout,
        }
    )


# ################################################################################
# # create_packed_image
# #
# # This function will take all the files within the resource_lists/[list]/items
# # and create a single packed image of them. Then return the coordinates so that
# # css can be written to load all of the images from the same file instead of
# # making a large number of get requests for the file
# ################################################################################
# def create_packed_image(calculator_name: str) -> Tuple[int, int, Dict[str, Tuple[int, int]]]:
def image_pack_function(input_files: MultiFile, output_files: ImagePackOutputFiles) -> None:
    output_image_path: str = output_files["image_file"]
    output_data_path: str = output_files["image_layout_file"]
    input_image_files: List[str] = input_files["files"]

    image_coordinates: Dict[str, Tuple[int, int]] = {}

    # Build tuple of simple names to filepaths
    images: List[Tuple[str, str]] = []
    for file in input_image_files:
        images.append((
            os.path.splitext(os.path.basename(file))[0],
            file
        ))

    # Open first image to get a standard
    first_image: Image.Image = Image.open(images[0][1])
    standard_width: int
    standard_height: int
    standard_width, standard_height = first_image.size
    standard_image_reference: str = images[0][1]

    # Sort the images, this is probably not necessary but will allow for
    # differences between files to be noticed with less noise of random shifting of squares
    images.sort(key=lambda x: x[0])

    # Use our special math function to determine what the number of columns
    # should be for the final packed image.
    # Programmers note: This was a lot of fun to figure out and derived strangely
    columns: int = math.ceil(math.sqrt(standard_height * len(images) / standard_width))
    result_width: int = standard_width * columns
    result_height: int = standard_height * math.ceil((len(images) / columns))

    # Determine where each image should go
    for index, (name, image) in enumerate(images):
        x_coordinate = (index % columns) * standard_width
        y_coordinate = math.floor(index / columns) * standard_height
        image_coordinates[name] = (x_coordinate, y_coordinate)

    # Create the new packed image file and all the coordinates of the images
    result = Image.new('RGBA', (result_width, result_height))
    for image_name, image_path in images:
        image_object = Image.open(image_path)
        width, height = image_object.size

        if (standard_width != width or standard_height != height):
            print("ERROR: All resource list item images for a single calculator must be the same size")
            print("       " + image_path + " and " + standard_image_reference + " are not the same size")

        x_coordinate, y_coordinate = image_coordinates[image_name]
        result.paste(im=image_object, box=(x_coordinate, y_coordinate))
    result.save(output_image_path)

    # Write the metadata for the packed image that will be used for later phases
    with open(output_data_path, 'w') as f:
        json.dump({
            "standard_width": standard_width,
            "standard_height": standard_height,
            "image_coordinates": image_coordinates
        }, f)



def image_compress_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    calculator_page = categories["calculator_dir"]

    output_calculator_imagefile = os.path.join("output", calculator_page, calculator_page + ".png")

    return (
        input_files,
        {
            "file": output_calculator_imagefile
        }
    )


def image_compress_function(input_files: SingleFile, output_files: SingleFile) -> None:
    input_file = input_files["file"]
    output_file = output_files["file"]

    # Copy the file
    shutil.copyfile(input_file, output_file)

    try:
        subprocess.run(["pngquant", "--force", "--ext", ".png", "256", "--nofs", output_file])
    except OSError as e:
        print("WARNING: PNG Compression Failed. This is non-critical in a development environment")
        print("        ", e)


def image_copy_function(input_file: str, match: re.Match, output_files: List[str]) -> None:
    # Sanity check that there is only one output
    if len(output_files) != 1:
        raise ValueError("Must copy " + input_file + " to only one location not" + str(output_files))
    output_file = output_files[0]

    # Copy the file
    shutil.copyfile(input_file, output_file)
