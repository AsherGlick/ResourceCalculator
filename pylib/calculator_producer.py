import shutil
import subprocess
import htmlmin  # type: ignore
from pylib.producers import Producer
from typing import List, Tuple, OrderedDict, Dict, Set
import re
import os
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, TokenError, Token, get_primitive
from pylib.yaml_token_load import ordered_load
from jinja2 import Environment, FileSystemLoader
import json
from pylib.uglifyjs import uglify_js_string
from pylib.json_data_compressor import mini_js_data
from pylib.webminify import minify_css_blocks


def calculator_producers() -> List[Producer]:
    return [
        Producer(
            input_path_patterns=[
                "^resource_lists/([a-z ]+)/resources.yaml$",
                "^cache/([a-z ]+)/packed_image_layout.json$",
                # "^core/calculator.html$", # TODO: Figure out how to support having a dependency that does not contain required information
            ],
            output_paths=calculator_output_paths,
            function=calculator_function,
            categories=["calculator"]
        )

    ]


def calculator_output_paths(path: str, match: re.Match) -> List[str]:
    calculator_page = match.group(1)

    calculator_index_page = os.path.join("output", calculator_page, "index.html")

    return [
        calculator_index_page,
    ]


# ################################################################################
# # create_calculator_page
# #
# # This function takes in a the name of a calculator resource list and creates
# # the html page and resource for it. If no files have been changed for the
# # calculator since the last time it was created then the creation will be skipped
# ################################################################################
def calculator_function(input_file: str, match: re.Match, output_files: List[str]) -> None:
    calculator_name: str = match.group(1)
    resource_list_file = os.path.join("resource_lists", calculator_name, "resources.yaml")
    image_metadata_file = os.path.join("cache", calculator_name, "packed_image_layout.json")
    input_files = [resource_list_file, image_metadata_file]

    if input_file not in input_files:
        raise ValueError("Expected the input file to be one of:" + str(input_files) + " but got" + input_file)

    if len(output_files) != 1:
        raise ValueError("Expected just one output file but got" + str(output_files))
    
    calculator_index_html_filepath = output_files[0]

    errors = []
    # calculator_folder = os.path.join("output", calculator_name)
    # source_folder = os.path.join("resource_lists", calculator_name)
    # if not os.path.exists(calculator_folder):
    #     os.makedirs(calculator_folder)
    # elif not force:
    #     oldest_output = get_oldest_modified_time(calculator_folder)
    #     newest_resource = get_newest_modified_time(source_folder)
    #     newest_corelib = get_newest_modified_time("core", ignore=["calculator.js", "calculator.js.map"])
    #     newest_build_script = os.path.getctime("build.py")
    #     newest_build_lib = get_newest_modified_time("pylib")

    #     if oldest_output > max(newest_resource, newest_corelib, newest_build_script, newest_build_lib):
    #         # Allow not printing the skip text for polling with the --watch flag
    #         if print_skip_text:
    #             print("Skipping", calculator_name, "Nothing has changed since the last build")
    #         return

    # start_time = time.time()

    print("Generating", calculator_name, "into", calculator_index_html_filepath)

#     # Create a packed image of all the item images
#     image_width: int
#     image_height: int
#     resource_image_coordinates: Dict[str, Tuple[int, int]]
#     image_width, image_height, resource_image_coordinates = create_packed_image(calculator_name)
    
    with open(image_metadata_file) as f:
        image_metadata = json.load(f)
        image_width = image_metadata["standard_width"]
        image_height = image_metadata["standard_height"]
        resource_image_coordinates = image_metadata["image_coordinates"]

    # Load in the yaml resources file
    resource_list, parse_errors = load_resource_list(resource_list_file)
    errors += parse_errors # todo: seperate out the resource list parsing and linting and just load this from json

    resources: OrderedDict[str, Resource] = resource_list.resources
    resources = expand_raw_resource(resources) # TODO: Move to linter
    resources = fill_default_requirement_groups(resources, resource_list.requirement_groups) # TODO: Move to linter/importer producer

    authors: OrderedDict[str, str] = resource_list.authors

    recipe_types: OrderedDict[str, str] = resource_list.recipe_types

    stack_sizes: OrderedDict[str, StackSize] = resource_list.stack_sizes

    errors += lint_resources(calculator_name, resources, recipe_types, stack_sizes) # TODO: Move to linter/importer producer

    default_stack_size: str = resource_list.default_stack_size

    # TODO: Add linting for stack sizes in linter/importer producer

    recipe_type_format_js = generate_recipe_type_format_js(calculator_name, recipe_types)
    recipe_type_format_js = uglify_js_string(recipe_type_format_js)

    recipe_js_data = mini_js_data(get_primitive(get_recipes_only(resources)), "recipe_json")

    html_resource_data = generate_resource_html_data(resources)

    item_styles = generate_resource_offset_classes(resources, resource_image_coordinates)

    # Generate some css to allow us to center the list
    content_width_css = generate_content_width_css(image_width, resource_list)

    stack_sizes = merge_custom_multipliers(stack_sizes, resources)

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
        authors=authors,
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


# TODO: MOVE ALL THIS TO THE EDITOR PRODUCER
#     resource_list_js_data = mini_js_data(hack_update_version(get_primitive(resource_list)), "resource_list_json")

#     editor_template = env.get_template("edit.html")

#     rendered_editor = editor_template.render(
#         resource_list_json=resource_list_js_data,
#         element_height=55,  # should be automatically generated from the image height? width? or should be static
#         total_height=55 * 989,  # Should be implemented in-javascript
#         buffer_element_count=2,
#     )

#     minified_editor = rendered_editor
#     # minified_editor = htmlmin.minify(rendered_editor, remove_comments=True, remove_empty_space=True)
#     # minified_editor = minify_css_blocks(minified_editor)

#     with open(os.path.join(calculator_folder, "edit.html"), "w", encoding="utf_8") as f:
#         f.write(minified_editor)

#     # Sanity Check Warning, is there an image that does not have a recipe
#     simple_resources = [x["simplename"] for x in html_resource_data]
#     for simple_name in resource_image_coordinates:
#         if simple_name not in simple_resources:
#             print("WARNING:", simple_name, "has an image but no recipe and will not appear in the calculator")

#     # Touch the created time of all the files in the output folder to prevent
#     # re-triggering generation on outdated files that were intentionally skipped
#     touch_output_folder_files(calculator_folder)

#     publish_calculator_plugins(calculator_folder, source_folder)

#     if len(errors) > 0:
#         with open(resource_list_file, 'r', encoding="utf_8") as f:
#             fulltext = f.read()
#             fulltext_lines = fulltext.split("\n")

#         for error in errors:
#             error.print_error(fulltext_lines)

#     end_time = time.time()
#     print("  Generated in %.3f seconds" % (end_time - start_time))




def load_resource_list(filepath: str) -> Tuple[ResourceList, List[TokenError]]:
    errors: List[TokenError] = []

    with open(filepath, 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    return (resource_list, errors)


# TODO: Move to linter/importer producer
################################################################################
# expand_raw_resource allow for the syntactic candy of only defining a a
# `recipe_type` value for raw resources and not having to define the entire
# construct because it is a trivial construct.
################################################################################
def expand_raw_resource(resources: OrderedDict[str, Resource]) -> OrderedDict[str, Resource]:
    for resource in resources:
        for i, recipe in enumerate(resources[resource].recipes):
            if recipe.recipe_type == "Raw Resource" and recipe.output == 0 and len(recipe.requirements) == 0:
                resources[resource].recipes[i].output = 1
                resources[resource].recipes[i].requirements = OrderedDict([(resource, 0)])
    return resources


# TODO: Move to linter/importer producer
################################################################################
# fill_default_requirement_groups replaces any uses of a requirement group with
# the first item within that requirement group. This is an interim solution
# while the requirement group feature is separately fleshed out. It has been
# included in this state because there is some simplicity value to being able
# to include the data structure in the resource_list.yaml file.
################################################################################
def fill_default_requirement_groups(resources: OrderedDict[str, Resource], requirement_groups: OrderedDict[str, List[str]]) -> OrderedDict[str, Resource]:
    for resource in resources:
        for i, recipe in enumerate(resources[resource].recipes):
            # Create a copy of the keys so we can iterate over them and mutate them
            requirement_list: List[str] = [requirement for requirement in recipe.requirements]

            # Iterate over the requirements and replace any that are part of requirement groups
            for requirement in requirement_list:
                if requirement in requirement_groups:
                    value = recipe.requirements[requirement]
                    del recipe.requirements[requirement]
                    recipe.requirements[requirement_groups[requirement][0]] = value
    return resources


# TODO: Move to linter/importer producer
################################################################################
#
################################################################################
def lint_resources(
    calculator_name: str,
    resources: OrderedDict[str, Resource],
    recipe_types: OrderedDict[str, str],
    stack_sizes: OrderedDict[str, StackSize]
) -> List[TokenError]:
    errors: List[TokenError] = []
    for resource in resources:
        errors += lint_recipes(calculator_name, resource, resources[resource].recipes)
        errors += lint_custom_stack_multipliers(calculator_name, resource, resources[resource].custom_stack_multipliers, stack_sizes)

    errors += ensure_valid_requirements(resources)
    errors += ensure_valid_recipe_types(calculator_name, resources, recipe_types)
    errors += ensure_unique_simple_names(calculator_name, resources)

    return errors


# TODO: Move to linter/importer producer
################################################################################
# lint_recipe
#
# This function takes in the name of the calculator, an item name, and the list
# of recipes to ensure that the given item's recipes all follow a set of
# patterns in order to make sure that all recipe lists are uniform in style
# and contents. In addition it makes sure that all of the required elements of
# a recipe are present and that no additional unknown elements are present.
################################################################################
def lint_recipes(calculator_name: str, item_name: str, recipes: List[Recipe]) -> List[TokenError]:
    errors: List[TokenError] = []

    # Check that every resource has a raw recipe
    raw_resource_count = 0
    for recipe in recipes:
        if (recipe.recipe_type == "Raw Resource"):
            if (recipe.output == 1 and recipe.requirements == OrderedDict([(item_name, 0)])):
                raw_resource_count += 1
            else:
                # TODO: Have a better token associated with this error
                errors.append(TokenError(item_name + " has an invalid \"Raw Resource\"", Token()))

    # Lint that every resource has a raw resource and only one
    if raw_resource_count == 0:
        # TODO: Have a better token associated with this error
        errors.append(TokenError(item_name + " must have a \"Raw Resource\" which outputs 1 and has a requirement of 0 of itself", Token()))
    elif raw_resource_count > 1:
        # TODO: Have a better token associated with this error
        errors.append(TokenError(item_name + " must have only one \"Raw Resource\"", Token()))

    return errors


# TODO: Move to linter/importer producer
################################################################################
#
################################################################################
def lint_custom_stack_multipliers(
    calculator_name: str,
    item_name: str,
    custom_stack_multipliers: OrderedDict[str, int],
    stack_sizes: OrderedDict[str, StackSize]
) -> List[TokenError]:
    errors: List[TokenError] = []
    for stack_name in custom_stack_multipliers:
        custom_size = custom_stack_multipliers[stack_name]

        if stack_name not in stack_sizes:
            # TODO: Have a better token associated with this error
            errors.append(TokenError("custom_stack_size \"" + stack_name + "\" for" + item_name + "is not a valid stack size. (" + ", ".join([x for x in stack_sizes]) + ")", Token()))

        if custom_size < 1:
            # TODO: Have a better token associated with this error
            errors.append(TokenError("custom_stack_size \"" + stack_name + "\" for" + item_name + "cannot be less than 1.", Token()))

    return errors




# TODO: Move to linter/importer producer
################################################################################
# ensure_valid_requirements
#
# Make sure each recipe requirement is another existing item in the resource list
################################################################################
def ensure_valid_requirements(resources: OrderedDict[str, Resource]) -> List[TokenError]:
    errors: List[TokenError] = []
    for resource in resources:
        for recipe in resources[resource].recipes:
            for requirement in recipe.requirements:
                if requirement not in resources:
                    # TODO: Have a better token associated with this error
                    errors.append(TokenError("ERROR: Invalid requirement for resource:" + resource + ". \"" + requirement + "\" does not exist as a resource", Token()))
                elif recipe.requirements[requirement] > 0:
                    # TODO: Have a better token associated with this error
                    errors.append(TokenError("ERROR: Invalid requirement for resource:" + resource + ". \"" + requirement + "\" must be a negative number", Token()))
    return errors


# TODO: Move to linter/importer producer
################################################################################
#
################################################################################
def ensure_valid_recipe_types(calculator_name: str, resources: OrderedDict[str, Resource], recipe_types: OrderedDict[str, str]) -> List[TokenError]:
    used_recipe_types: Set[str] = set()
    errors: List[TokenError] = []

    for resource in resources:
        for recipe in resources[resource].recipes:
            recipe_type: str = recipe.recipe_type

            # add this to the list of found recipe types to later check to make sure all the recipe_types in the list are used
            if recipe_type != "Raw Resource":
                used_recipe_types.add(recipe_type)

            # check if this recipe exists in the recipe type list
            if recipe_type not in recipe_types and recipe_type != "Raw Resource":
                # TODO: Have a better token associated with this error
                errors.append(TokenError(resource + " has an undefined resource_type" + ": \"" + recipe_type + "\"", Token()))

    for recipe_type in recipe_types:
        if recipe_type not in used_recipe_types:
            errors.append(TokenError("Unused recipe_type \"" + recipe_type + "\"", Token()))

    return errors


# TODO: Move to linter/importer producer
################################################################################
#
################################################################################
def ensure_unique_simple_names(calculator_name: str, resources: OrderedDict[str, Resource]) -> List[TokenError]:
    errors: List[TokenError] = []
    simple_names: Dict[str, List[str]] = {}

    for resource in resources:
        simple_name: str = get_simple_name(resource, resources)
        if simple_name not in simple_names:
            simple_names[simple_name] = []
        simple_names[simple_name].append(resource)

    for simple_name in simple_names:
        if len(simple_names[simple_name]) > 1:
            # TODO: Have a better token associated with this error
            errors.append(TokenError(", ".join(simple_names[simple_name]) + "all share the same simple name" + simple_name, Token()))

    return errors



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
def generate_recipe_type_format_js(calculator_name: str, recipe_types: OrderedDict[str, str]) -> str:
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
