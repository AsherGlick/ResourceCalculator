from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Tuple, TypedDict
import json
import os
from pylib.filehash import getfilehash
from pylib.producer import Producer, SingleFile, filename_from_metadatafile, GenericProducer
import shutil



class SingleHashedFile(TypedDict):
    file: str
    filemetadata: str

################################################################################
# LandingPageInputTypes
#
# A TypedDict representing the input files structure for the producer that
# creates the landing page.
################################################################################
class LandingPageInputTypes(TypedDict):
    files: List[str]
    icon_filename_data: List[str]
    css_filename_data: str
    add_game_filename_data: str
    template: str

################################################################################
# landing_page_producers
#
# Creates producers for generating the landing page and copying the icons that
# are used on the landing page.
################################################################################
def landing_page_producers(calculator_dir_regex: str) -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                "file": r"^resource_lists/(?P<calculator_dir>{calculator_dir_regex})/icon\.jpg$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
            },
            paths=logo_copy_paths,
            function=hash_and_copy_file,
            categories=["landing"],
        ),

        Producer(
            input_path_patterns={
                "files": [r"^cache/(?:{calculator_dir_regex})/page_metadata\.json$".format(
                    calculator_dir_regex=calculator_dir_regex
                )],
                "icon_filename_data": [r"^cache/(?:{calculator_dir_regex})/icon\.jpg_name\.json$".format(
                    calculator_dir_regex=calculator_dir_regex
                )],
                "css_filename_data": r"^cache/calculator\.css\.json",
                "add_game_filename_data": r"^cache/add_game\.png\.json$",
                "template": r"^core/index\.html$"
            },
            paths=landing_page_paths,
            function=landing_page_function,
            categories=["landing"],
        )
    ]


################################################################################
# hash_and_copy_file
#
# Copies a file with a dynamic output and saves a file with that dynamic output
# in a fixed location for later lookups
################################################################################
def hash_and_copy_file(input_files: SingleFile, output_files: SingleHashedFile) -> None:
    input_file: str = input_files["file"]
    output_file: str = output_files["file"]

    output_metadata_file: str = output_files["filemetadata"]

    # Copy the file
    shutil.copyfile(input_file, output_file)

    # Write the hashed file name to a known location
    with open(output_metadata_file, 'w') as f:
        json.dump({
            "icon_name": output_file
        }, f)




################################################################################
# logo_copy_paths
#
# The input and output paths generation function for copying icon files into the
# output directory.
################################################################################
def logo_copy_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleHashedFile]:
    calculator_name = categories["calculator_dir"]

    logo_path = input_files["file"]

    filehash = getfilehash(logo_path)

    return (
        input_files,
        {
            "file": os.path.join("output", calculator_name, "icon-" + filehash + ".jpg"),
            "filemetadata": os.path.join("cache", calculator_name, "icon.jpg_name.json"),
        }
    )





################################################################################
# landing_page_paths
#
# The input and output paths generation function for creating a landing page.
################################################################################
def landing_page_paths(input_files: LandingPageInputTypes, categories: Dict[str, str]) -> Tuple[LandingPageInputTypes, SingleFile]:
    return (
        input_files,
        {
            "file": "output/index.html"
        }
    )


################################################################################
# landing_page_function
#
# The function that generates the landing page output file that links to each
# of the calculator pages.
################################################################################
def landing_page_function(input_paths: LandingPageInputTypes, output_paths: SingleFile) -> None:

    # Configure and begin the jinja2 template parsing
    env = Environment(loader=FileSystemLoader('core'))
    template = env.get_template("index.html")

    icon_filename_datas: Dict[str, str] = {}

    for icon_filename_data in input_paths["icon_filename_data"]:
        icon_filename_datas[os.path.basename(os.path.dirname(icon_filename_data))] = icon_filename_data

    calculators = []
    for metadata_path in input_paths["files"]:

        with open(metadata_path) as f:
            calculator_display_name = json.load(f)["calculator_name"]

        directory = os.path.basename(os.path.dirname(metadata_path))

        icon_filename_data = icon_filename_datas[directory]


        with open(icon_filename_data) as f:
            icon_filename = os.path.basename(json.load(f)["icon_name"])

        calculator_data = {
            "path": directory,
            "display_name": calculator_display_name,
            "icon_filename": icon_filename
        }

        calculators.append(calculator_data)

    add_game_image_path = filename_from_metadatafile(input_paths["add_game_filename_data"], rel="output")
    css_path = filename_from_metadatafile(input_paths["css_filename_data"], rel="output")

    output_from_parsed_template = template.render(
        calculators=calculators,
        addgame_image_path=add_game_image_path,
        css_path=css_path,
    )

    with open(os.path.join(output_paths["file"]), "w", encoding="utf_8") as f:
        f.write(output_from_parsed_template)
