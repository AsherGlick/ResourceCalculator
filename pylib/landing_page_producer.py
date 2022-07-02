from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, Tuple, TypedDict
import json
import os

from pylib.producer import Producer, SingleFile, producer_copyfile, GenericProducer


################################################################################
# landing_page_producers
#
# Creates producers for generating the landing page and copying the icons that
# are used on the landing page.
################################################################################
def landing_page_producers() -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                "file": r"^resource_lists/(?P<calculator_dir>[a-z ]+)/icon\.png$",
            },
            paths=logo_copy_paths,
            function=producer_copyfile,
            categories=["landing"],
        ),

        Producer(
            input_path_patterns={
                "files": [r"^cache/[a-z ]+/page_metadata\.json$"],
                "template": r"^core/index\.html$"
            },
            paths=landing_page_paths,
            function=landing_page_function,
            categories=["landing"],
        )
    ]


################################################################################
# logo_copy_paths
#
# The input and output paths generation function for copying icon files into the
# output directory.
################################################################################
def logo_copy_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    calculator_name = categories["calculator_dir"]
    return (
        input_files,
        {
            "file": os.path.join("output", calculator_name, "icon.png")
        }
    )


################################################################################
# LandingPageInputTypes
#
# A TypedDict representing the input files structure for the producer that
# creates the landing page.
################################################################################
class LandingPageInputTypes(TypedDict):
    files: List[str]
    template: str


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

    calculators = []
    for metadata_path in input_paths["files"]:

        with open(metadata_path) as f:
            calculator_display_name = json.load(f)["calculator_name"]

        directory = os.path.basename(os.path.dirname(metadata_path))

        calculator_data = {
            "path": directory,
            "display_name": calculator_display_name
        }

        calculators.append(calculator_data)

    output_from_parsed_template = template.render(calculators=calculators)

    with open(os.path.join(output_paths["file"]), "w", encoding="utf_8") as f:
        f.write(output_from_parsed_template)
