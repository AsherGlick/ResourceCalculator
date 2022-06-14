import htmlmin  # type: ignore
from pylib.producers import Producer, SingleFile
from typing import List, Tuple, OrderedDict, Dict, TypedDict, Tuple
import re
import os
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, get_primitive
from jinja2 import Environment, FileSystemLoader
import json
from pylib.uglifyjs import uglify_js_string
from pylib.json_data_compressor import mini_js_data
from pylib.webminify import minify_css_blocks
import pickle

def calculator_producers() -> List[Producer]:
    return [
        Producer(
            input_path_patterns=[
                "^cache/([a-z ]+)/resources.pickle$",
                "^cache/([a-z ]+)/packed_image_layout.json$",
            ],
            paths=calculator_paths,
            function=calculator_function,
            categories=calculator_categories,
        )

    ]


class CalculatorInputFile(TypedDict):
    resources_pickle: str
    image_layout_json: str
    calculator_template: str

def calculator_categories(input_files: CalculatorInputFile) -> List[str]:
    return ["calculator"]

def calculator_paths(index: int, regex: str, match: re.Match) -> Tuple[CalculatorInputFile, SingleFile]:
    calculator_page = match.group(1)
    calculator_index_page = os.path.join("output", calculator_page, "index.html")

    return (
        {
            "resources_pickle": os.path.join("cache", calculator_page, "resources.pickle"),
            "image_layout_json": os.path.join("cache", calculator_page, "packed_image_layout.json"),

            # TODO: Are there other template files that should be added here too?
            "calculator_template": "core/calculator.html",
        },{
            "file": calculator_index_page

        })


# ################################################################################
# # create_calculator_page
# #
# # This function takes in a the name of a calculator resource list and creates
# # the html page and resource for it. If no files have been changed for the
# # calculator since the last time it was created then the creation will be skipped
# ################################################################################
def calculator_function(input_files: CalculatorInputFile, output_files: SingleFile) -> None:

    resource_list_file = input_files["resources_pickle"] # os.path.join("cache", calculator_name, "resources.pickle")
    image_metadata_file = input_files["image_layout_json"] #os.path.join("cache", calculator_name, "packed_image_layout.json")

    match = re.match(r"^cache/([a-z ]+)/resources.pickle$", resource_list_file)
    if match is None:
        raise ValueError
    calculator_name = match.group(1)


    calculator_index_html_filepath = output_files["file"]

    # print("Generating", calculator_name, "into", calculator_index_html_filepath)

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

    recipe_type_format_js = generate_recipe_type_format_js(resource_list.recipe_types)
    recipe_type_format_js = uglify_js_string(recipe_type_format_js)

    recipe_js_data = mini_js_data(get_primitive(get_recipes_only(resource_list.resources)), "recipe_json")

    html_resource_data = generate_resource_html_data(resource_list.resources)

    item_styles = generate_resource_offset_classes(resource_list.resources, resource_image_coordinates)

    # Generate some css to allow us to center the list
    content_width_css = generate_content_width_css(image_width, resource_list)

    stack_sizes = merge_custom_multipliers(stack_sizes, resource_list.resources)

    stack_sizes_json = json.dumps(get_primitive(stack_sizes))

    # Generate the calculator from a template
    env = Environment(loader=FileSystemLoader('core'))
    calculator_template = env.get_template("calculator.html")
    rendered_calculator = calculator_template.render(
        # A simplified list used for creating the item selector HTML
        resources=html_resource_data,
        # the javascript/json object used for calculations
        recipe_json=recipe_js_data,
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
        stack_sizes_json=stack_sizes_json)

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
# generate_recipe_type_format_js
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
                    print("UNKNOWN IDENTIFIER IN FORMAT STRING", chunk)  # TODO makethis error message better

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
#
################################################################################
def get_recipes_only(resources: OrderedDict[str, Resource]) -> Dict[str, List[Recipe]]:
    return {resource: resources[resource].recipes for resource in resources}


################################################################################
# generate_resource_html_data
#
#
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
#
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
#
################################################################################
def merge_custom_multipliers(stack_sizes: OrderedDict[str, StackSize], resources: OrderedDict[str, Resource]) -> OrderedDict[str, StackSize]:
    for resource in resources:
        custom_sizes = resources[resource].custom_stack_multipliers
        for custom_size_name in custom_sizes:
            custom_size = custom_sizes[custom_size_name]

            stack_sizes[custom_size_name].custom_multipliers[resource] = custom_size

    return stack_sizes
