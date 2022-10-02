from jinja2 import Environment, FileSystemLoader
from typing import List, Tuple, OrderedDict, Dict, TypedDict
import htmlmin  # type: ignore
import json
import os
import pickle
import re

from pylib.json_data_compressor import mini_js_data
from pylib.producer import Producer, SingleFile, GenericProducer, filename_from_metadatafile
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, get_primitive
from pylib.uglifyjs import uglify_js_string
from pylib.webminify import minify_css_blocks


################################################################################
# calculator_producer
#
# Creates producers for generating the calculator pages.
################################################################################
def calculator_producers(calculator_dir_regex: str) -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                "resources_pickle": r"^cache/(?P<calculator_dir>{calculator_dir_regex})/resources\.pickle$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
                "image_layout_json": r"^cache/(?P<calculator_dir>{calculator_dir_regex})/packed_image_layout\.json$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
                "css_filename_data": r"^cache/calculator\.css\.json",
                "calculator_template": r"^core/calculator\.html$"
            },
            paths=calculator_paths,
            function=calculator_function,
            categories=["calculator"],
        )

    ]


################################################################################
# CalculatorInputFiles
#
# A TypedDict representing the input files structure for the producer that
# creates the calculator pages.
################################################################################
class CalculatorInputFiles(TypedDict):
    resources_pickle: str
    image_layout_json: str
    css_filename_data: str
    calculator_template: str


################################################################################
# calculator_paths
#
# The input and output paths generation function for creating calculator pages.
################################################################################
def calculator_paths(input_files: CalculatorInputFiles, categories: Dict[str, str]) -> Tuple[CalculatorInputFiles, SingleFile]:
    calculator_page = categories["calculator_dir"]
    calculator_index_page = os.path.join("output", calculator_page, "index.html")

    return (
        input_files,
        {
            "file": calculator_index_page
        }
    )


################################################################################
# calculator_function
#
# This function takes in a the input and output paths for the calculator
# producer and writes the html page and resource for it to the output file.
################################################################################
def calculator_function(input_files: CalculatorInputFiles, output_files: SingleFile) -> None:

    resource_list_file = input_files["resources_pickle"]
    image_metadata_file = input_files["image_layout_json"]

    match = re.match(r"^cache/([a-z ]+)/resources.pickle$", resource_list_file)
    if match is None:
        raise ValueError
    calculator_name = match.group(1)

    calculator_index_html_filepath = output_files["file"]

    with open(image_metadata_file) as f:
        image_metadata = json.load(f)
        image_width = image_metadata["standard_width"]
        image_height = image_metadata["standard_height"]
        resource_image_coordinates = image_metadata["image_coordinates"]

    # Load and validate the type of the resource list data
    with open(resource_list_file, 'rb') as f:
        resource_list = pickle.load(f)
        if not isinstance(resource_list, ResourceList):
            raise ValueError("Pickled Resource List File is not a valid ResourceList class")

    stack_sizes: OrderedDict[str, StackSize] = resource_list.stack_sizes

    default_stack_size: str = resource_list.default_stack_size

    resource_simple_names_js_data = mini_js_data(get_primitive(get_simple_names_only(resource_list.resources)), "resource_simple_names")

    recipe_type_format_js = generate_recipe_type_format_js(resource_list.recipe_types)
    recipe_type_format_js = uglify_js_string(recipe_type_format_js)

    recipe_js_data = mini_js_data(get_primitive(get_recipes_only(resource_list.resources)), "recipe_json")

    html_resource_data = generate_resource_html_data(resource_list.resources)

    item_styles = generate_resource_offset_classes(resource_list.resources, resource_image_coordinates)

    # Generate some css to allow us to center the list
    content_width_css = generate_content_width_css(image_width, resource_list)

    stack_sizes = merge_custom_multipliers(stack_sizes, resource_list.resources)

    stack_sizes_json = json.dumps(get_primitive(stack_sizes))

    css_path = filename_from_metadatafile(input_files["css_filename_data"], rel=os.path.dirname(calculator_index_html_filepath))

    # Generate the calculator from a template
    env = Environment(loader=FileSystemLoader('core'))
    calculator_template = env.get_template("calculator.html")
    rendered_calculator = calculator_template.render(
        # A simplified list used for creating the item selector HTML
        resources=html_resource_data,
        # the javascript/json object used for calculations
        recipe_json=recipe_js_data,
        # names for proper image mapping
        resource_simple_names=resource_simple_names_js_data,
        # The size and positions of the image
        item_width=image_width,
        item_height=image_height,
        item_styles=item_styles,
        # The name of the calculator
        resource_list=calculator_name,
        # Javascript formatting functions for recipe instructions # TODO this should be made into format strings to save space
        recipe_type_format_js=recipe_type_format_js,
        # The list of authors and emails to display in the authors sections
        authors=resource_list.authors,
        # Additional CSS to center the list when resizing
        content_width_css=content_width_css,
        # Used to build the stack size selector UI
        stack_sizes=stack_sizes,
        default_stack_size=default_stack_size,
        # Used to do calculations to divide counts into stacks
        stack_sizes_json=stack_sizes_json,
        css_path=css_path,
    )

    minified_calculator = htmlmin.minify(rendered_calculator, remove_comments=True, remove_empty_space=True)
    minified_calculator = minify_css_blocks(minified_calculator)

    with open(calculator_index_html_filepath, "w", encoding="utf_8") as f:
        f.write(minified_calculator)

    # Sanity Check Warning, is there an image that does not have a recipe
    simple_resources = [x["simplename"] for x in html_resource_data]
    for simple_name in resource_image_coordinates:
        if simple_name not in simple_resources:
            print("WARNING:", simple_name, "has an image but no recipe and will not appear in the calculator")


# TODO: Move to shared library to be used in other places?
################################################################################
# get_simple_name checks if a simple name override has been set for the
# resource, and if it has then returns it. Otherwise it generates the simple
# name from the resource's actual name.
################################################################################
def get_simple_name(resource: str, resources: OrderedDict[str, Resource]) -> str:
    # TODO: Change this if we end up implementing something like "is_set()" for the YAML conversions
    if resources[resource].custom_simplename != "":
        return resources[resource].custom_simplename
    return re.sub(r'[^a-z0-9]', '', resource.lower())

################################################################################
# get_simple_names_only generates an object of custom_simplenames only for
# resources where a simple name override has been set.
################################################################################
def get_simple_names_only(resources: OrderedDict[str, Resource]) -> Dict[str, str]:
    simple_names = {}

    for resourceKey in resources:
        if resources[resourceKey].custom_simplename != "":
            simple_names[resourceKey] = resources[resourceKey].custom_simplename

    return simple_names

################################################################################
# generate_recipe_type_format_js
#
# TODO: Investigate this function, it did not originally have a descriptive
# comment and now the following Example Output might not be accurate to the
# function.
#
# Example output:
#
# [{
#         "name":
#         "tokenized_inputs": []
#         "input_chunks": [
#             {
#                 "type":"text",
#                 "text":"Craft"
#             },
#             {
#                 "type":"output"
#             }
#             {
#                 "type":"all_other_inputs"
#             }
#             {
#                 "type":"tokenized_input",
#                 "name":"Fuel"
#             }
#         ]
#     }]
################################################################################
def generate_recipe_type_format_js(recipe_types: OrderedDict[str, str]) -> str:
    recipe_type_format_functions = []

    for recipe_type in recipe_types:
        recipe_type_format_string = recipe_types[recipe_type]

        all_chunks = re.split('({[^}]+})', recipe_type_format_string)

        tokenized_inputs = []
        input_chunks = []

        for chunk in all_chunks:
            if len(chunk) < 1:
                continue

            if chunk.startswith("{") and chunk.endswith("}"):
                chunk = chunk[1:-1]

                if chunk == "IN_ITEMS":
                    input_chunks.append({"type": "all_other_inputs"})
                elif chunk == "OUT_ITEM":
                    input_chunks.append({"type": "output"})
                elif chunk.startswith("ITEM"):
                    tokenized_item_name = chunk[5:]
                    input_chunks.append({"type": "tokenized_input", "name": tokenized_item_name})
                    tokenized_inputs.append(tokenized_item_name)
                    # TODO: some linting here can be done to make sure that all recipe_types that have this tokenized item have the item
                else:
                    print("UNKNOWN IDENTIFIER IN FORMAT STRING", chunk)  # TODO make this error message better

            else:
                input_chunks.append({"type": "text", "text": chunk})

        format_function = {
            "name": recipe_type,
            "tokenized_inputs": json.dumps(tokenized_inputs),
            "input_chunks": input_chunks
        }

        recipe_type_format_functions.append(format_function)

    env = Environment(loader=FileSystemLoader('core'))
    template = env.get_template("_recipe_type_display_functions.js")

    return template.render(recipe_type_format_functions=recipe_type_format_functions)


################################################################################
# get_recipes_only
#
# Takes in a complete resources list and returns a mapping of each item to only
# the recipes that item has, stripping out all other information.
################################################################################
def get_recipes_only(resources: OrderedDict[str, Resource]) -> Dict[str, List[Recipe]]:
    return {resource: resources[resource].recipes for resource in resources}


################################################################################
# generate_resource_html_data
#
# Extracts a list of dicts containing information about each item that should
# be displayed to the user.
################################################################################
def generate_resource_html_data(resources: OrderedDict[str, Resource]) -> List[Dict[str, str]]:
    resources_html_data = []
    for resource in resources:
        resource_html_data = {}
        simple_name = get_simple_name(resource, resources)
        resource_html_data["aria_label"] = resource
        resource_html_data["simplename"] = simple_name
        resources_html_data.append(resource_html_data)
    return resources_html_data


################################################################################
# generate_resource_offset_classes
#
# Creates the CSS required to properly display images contained in the packed
# image.
################################################################################
def generate_resource_offset_classes(resources: OrderedDict[str, Resource], resource_image_coordinates: Dict[str, Tuple[int, int]]) -> Dict[str, str]:
    item_styles: Dict[str, str] = {}
    for resource in resources:
        simple_name = get_simple_name(resource, resources)

        if simple_name in resource_image_coordinates:
            x_coordinate, y_coordinate = resource_image_coordinates[simple_name]
            item_styles[simple_name] = "background-position: " + str(-x_coordinate) + "px " + str(-y_coordinate) + "px;"
        else:
            item_styles[simple_name] = "background: #f0f; background-image: none;"
            print("WARNING:", simple_name, "has a recipe but no image and will appear purple in the calculator")

    return item_styles


################################################################################
# generate_content_width_css
#
# Generates a series of content widths for the items to allow for the items to
# be centered on screen and to allow for more precise line wrapping if the
# row_group_count value is specified.
################################################################################
def generate_content_width_css(image_width: int, resource_list: ResourceList) -> str:
    content_width_css = ""
    media_padding = 40  # This give a slight padding from the edges, useful for avoiding intersection with scroll bars

    row_group_count = resource_list.row_group_count

    iteration = 1
    image_width_with_padding = image_width + 6  # TODO: This will need to be updated if custom styling is added to the calculator
    while iteration * row_group_count * image_width_with_padding < 3840:
        content_width = iteration * row_group_count * image_width_with_padding
        screen_max = (iteration + 1) * row_group_count * image_width_with_padding
        new_css = "@media only screen and (max-width: {}px) and (min-width:{}px) {{ .resource_content {{ width: {}px}}  }}".format(
            str(screen_max + media_padding - 1),
            str(content_width + media_padding),
            str(content_width),
        )

        content_width_css += new_css
        iteration += 1
    # When the width is less then a single group we still want the list to be centered
    for i in range(1, row_group_count):
        content_width = i * image_width_with_padding
        screen_max = (i + 1) * image_width_with_padding
        new_css = "@media only screen and (max-width: {}px) and (min-width:{}px) {{ .resource_content {{ width: {}px}}  }}".format(
            str(screen_max + media_padding - 1),
            str(content_width + media_padding),
            str(content_width),
        )

        content_width_css += new_css

    return content_width_css


################################################################################
# merge_custom_multipliers
#
# Takes the custom stack sizes found attached to each item and merges them into
# the stack size information so it can be displayed more easily.
################################################################################
def merge_custom_multipliers(stack_sizes: OrderedDict[str, StackSize], resources: OrderedDict[str, Resource]) -> OrderedDict[str, StackSize]:
    for resource in resources:
        custom_sizes = resources[resource].custom_stack_multipliers
        for custom_size_name in custom_sizes:
            custom_size = custom_sizes[custom_size_name]

            stack_sizes[custom_size_name].custom_multipliers[resource] = custom_size

    return stack_sizes
