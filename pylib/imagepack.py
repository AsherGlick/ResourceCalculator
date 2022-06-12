import shutil
import subprocess
from pylib.producers import Producer
from typing import List, Dict, Tuple
import re
import os
import math
import json
from PIL import Image  # type: ignore


def item_image_producers() -> List[Producer]:
    return [
        Producer(
            input_path_patterns=["^resource_lists/([a-z ]+)/items/.+$"],
            output_paths=image_pack_output_paths,
            function=image_pack_function,
            categories=["image"]
        ),

        Producer(
            input_path_patterns=["^cache/([a-z ]+)/items/packed_image.png$"],
            output_paths=image_compress_output_paths,
            function=image_compress_function,
            categories=["image", "compress", "imagecompress"]
        )
    ]

def image_pack_output_paths(path: str, match: re.Match) -> List[str]:
    calculator_page = match.group(1)

    calculator_imagefile = os.path.join("cache", calculator_page, "packed_image.png")
    calculator_image_layout = os.path.join("cache", calculator_page, "packed_image_layout.json")

    return [
        calculator_imagefile,
        calculator_image_layout,
    ]


# ################################################################################
# # create_packed_image
# #
# # This function will take all the files within the resource_lists/[list]/items
# # and create a single packed image of them. Then return the coordinates so that
# # css can be written to load all of the images from the same file instead of
# # making a large number of get requests for the file
# ################################################################################
# def create_packed_image(calculator_name: str) -> Tuple[int, int, Dict[str, Tuple[int, int]]]:

def image_pack_function(input_file: str, match: re.Match, output_files: List[str]) -> None:

    if len(output_files) != 2:
        raise ValueError("Expecting a output image file and an output data file. Instead got", output_files)

    output_image_path: str = output_files[0]
    output_data_path: str = output_files[1]

    calculator_name:str = match.group(1)

    resource_image_folder: str = os.path.join("resource_lists", calculator_name, "items")

    image_coordinates: Dict[str, Tuple[int, int]] = {}


    images: List[Tuple[str, str]] = []

    for file in os.listdir(resource_image_folder):
        images.append((
            os.path.splitext(file)[0],
            os.path.join(resource_image_folder, file)
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

    # # Create a new output file and write all the images to spots in the file
    # calculator_folder = os.path.join("output", calculator_name)
    # output_image_path = os.path.join(calculator_folder, calculator_name + ".png")

    # should_create_image = True

    # if os.path.exists(output_image_path):
#         newest_file = max(
#             os.path.getctime("build.py"),  # Check generator code modification
#             get_newest_modified_time("pylib"),  # Check generator code modification
#             get_newest_modified_time(resource_image_folder),  # Check source image modification
#         )
#         should_create_image = newest_file > os.path.getctime(output_image_path)

#     # Create or skip creation of the packed image
#     if should_create_image or FLAG_force_image:

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


    # Write the ata
    with open(output_data_path, 'w') as f:
        json.dump({
            "standard_width": standard_width,
            "standard_height": standard_height,
            "image_coordinates": image_coordinates
        }, f)


#     # image_width, image_height, resource_image_coordinates

















def image_compress_output_paths(path: str, match: re.Match) -> List[str]:
    calculator_page = match.group(1)

    calculator_imagefile = os.path.join("output", calculator_page, calculator_page + ".png")

    return [
        calculator_imagefile
    ]


def image_compress_function(input_file: str, match: re.Match, output_files: List[str]) -> None:
    # TODO: Acutally compress the file. This should become the "skip"/"fast" function

    # Sanity check that there is only one output
    if len(output_files) != 1:
        raise ValueError("Must copy " + input_file + " to only one location not" + str(output_files))
    output_file = output_files[0]

    # Copy the file
    shutil.copyfile(input_file, output_file)

        # try:
        #     subprocess.run(["pngquant", "--force", "--ext", ".png", "256", "--nofs", output_image_path])
        # except OSError as e:
        #     print("WARNING: PNG Compression Failed")
        #     print("        ", e)

