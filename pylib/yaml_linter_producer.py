from typing import List, Dict, Tuple, TypedDict, OrderedDict, Set
import json
import os
import pickle
import re

from pylib.producer import Producer, SingleFile, GenericProducer
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, TokenError, Token
from pylib.yaml_token_load import ordered_load


################################################################################
# resource_list_parser_producers
#
# Creates the producers for parsing resource lists and checking it for errors
# then outputing it as a python pickle file.
################################################################################
def resource_list_parser_producers(calculator_dir_regex: str) -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                "file": r"^resource_lists/(?P<calculator_dir>{calculator_dir_regex})/resources.yaml$".format(
                    calculator_dir_regex=calculator_dir_regex
                )
            },
            paths=resource_list_paths,
            function=resource_list_parser_function,
            categories=["resource_list"]
        ),
    ]


################################################################################
# ResourceListOutputFiles
#
# A TypedDict representing the output files structure for the producers that
# create the pre-parsed resource list files.
################################################################################
class ResourceListOutputFiles(TypedDict):
    resource_cache: str
    page_metadata: str


################################################################################
# resource_list_paths
#
# The input and output paths generation function for the producers that create
# pre-parsed and validated resource list files.
################################################################################
def resource_list_paths(input_files: SingleFile, categories: Dict[str, str]) -> Tuple[SingleFile, ResourceListOutputFiles]:
    calculator_page = categories["calculator_dir"]

    calculator_resource_cache = os.path.join("cache", calculator_page, "resources.pickle")
    calculator_page_metadata = os.path.join("cache", calculator_page, "page_metadata.json")

    return (
        input_files,
        {
            "resource_cache": calculator_resource_cache,
            "page_metadata": calculator_page_metadata,
        }
    )


################################################################################
# resource_list_parser_function
#
# This function is called by the producers to parse an input resource list
# and run all the validation on it.
################################################################################
def resource_list_parser_function(input_files: SingleFile, output_files: ResourceListOutputFiles) -> None:
    input_file = input_files["file"]
    resource_cache_path = output_files["resource_cache"]
    page_metadata_path = output_files["page_metadata"]

    errors = []

    resource_list: ResourceList

    resource_list, parse_errors = load_resource_list(input_file)
    errors += parse_errors

    resources: OrderedDict[str, Resource] = resource_list.resources
    resource_list.resources = expand_raw_resource(resource_list.resources)
    resource_list.resources = fill_default_requirement_groups(resource_list.resources, resource_list.requirement_groups)

    errors += lint_resources(resources, resource_list.recipe_types, resource_list.stack_sizes)

    # TODO: Add linting for stack sizes in linter/importer producer

    # Print errors if they exist
    if len(errors) > 0:
        with open(input_file, 'r', encoding="utf_8") as f:
            fulltext = f.read()
            fulltext_lines = fulltext.split("\n")

        for error in errors:
            error.print_error(fulltext_lines)

    # Output the completed datafiles
    with open(resource_cache_path, 'wb') as f:
        pickle.dump(resource_list, f)

    with open(page_metadata_path, 'w') as f:
        json.dump({
            "calculator_name": resource_list.index_page_display_name
        }, f)


def load_resource_list(filepath: str) -> Tuple[ResourceList, List[TokenError]]:
    errors: List[TokenError] = []

    with open(filepath, 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    return (resource_list, errors)


################################################################################
# expand_raw_resources
#
# expand_raw_resource allows for the syntactic candy of only defining a a
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


################################################################################
# fill_default_requirement_groups
#
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


################################################################################
# lint_resources
#
# Runs all of the linters used for resource objects in the recipe list.
################################################################################
def lint_resources(
    resources: OrderedDict[str, Resource],
    recipe_types: OrderedDict[str, str],
    stack_sizes: OrderedDict[str, StackSize]
) -> List[TokenError]:
    errors: List[TokenError] = []
    for resource in resources:
        errors += lint_recipes(resource, resources[resource].recipes)
        errors += lint_custom_stack_multipliers(resource, resources[resource].custom_stack_multipliers, stack_sizes)

    errors += ensure_valid_requirements(resources)
    errors += ensure_valid_recipe_types(resources, recipe_types)
    errors += ensure_unique_simple_names(resources)

    return errors


################################################################################
# lint_recipe
#
# This function takes in the name of the calculator, an item name, and the list
# of recipes to ensure that the given item's recipes all follow a set of
# patterns in order to make sure that all recipe lists are uniform in style
# and contents. In addition it makes sure that all of the required elements of
# a recipe are present and that no additional unknown elements are present.
################################################################################
def lint_recipes(item_name: str, recipes: List[Recipe]) -> List[TokenError]:
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


################################################################################
# lint_custom_stack_multipliers
#
# Lints that the definitions for custom stack multipliers all have proper
# values and don't reference non existant parent stack sizes.
################################################################################
def lint_custom_stack_multipliers(
    item_name: str,
    custom_stack_multipliers: OrderedDict[str, int],
    stack_sizes: OrderedDict[str, StackSize]
) -> List[TokenError]:
    errors: List[TokenError] = []
    for stack_name in custom_stack_multipliers:
        custom_size = custom_stack_multipliers[stack_name]

        if stack_name not in stack_sizes:
            # TODO: Have a better token associated with this error
            errors.append(TokenError(
                "custom_stack_size \"{stack_name}\" for {item_name} is not a valid stack size. ({stack_sizes})".format(
                    stack_name=stack_name,
                    item_name=item_name,
                    stack_sizes=", ".join([x for x in stack_sizes]),
                ),
                Token()
            ))

        if custom_size < 1:
            # TODO: Have a better token associated with this error
            errors.append(TokenError(
                "custom_stack_size \"{stack_name}\" for {item_name} cannot be less than 1.".format(
                    stack_name=stack_name,
                    item_name=item_name
                ),
                Token()
            ))

    return errors


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


################################################################################
# ensure_valid_recipe_types
#
# Validates that each defined recipe has a recipe type that exists.
################################################################################
def ensure_valid_recipe_types(resources: OrderedDict[str, Resource], recipe_types: OrderedDict[str, str]) -> List[TokenError]:
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


################################################################################
# ensure_unique_simple_names
#
# Validates that all the simple names are unique, otherwise there will be
# multiple items that share an image and provide ambiguous lookups.
################################################################################
def ensure_unique_simple_names(resources: OrderedDict[str, Resource]) -> List[TokenError]:
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
