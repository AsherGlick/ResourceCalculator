from typing import List, Dict, Tuple, OrderedDict, Set
import json
import os
import pickle
import re

from pylib.producer import Producer, SingleFile, GenericProducer
from pylib.resource_list import Heading, ResourceList, Resource, StackSize, Recipe, TokenError, Token
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
            name="Parse Resource List",
            input_path_patterns={
                "file": r"^resource_lists/(?P<calculator_dir>{calculator_dir_regex})/resources.yaml$".format(
                    calculator_dir_regex=calculator_dir_regex
                )
            },
            function=resource_list_parser_function,
        ),
    ]


################################################################################
# resource_list_parser_function
#
# This function is called by the producers to parse an input resource list
# and run all the validation on it.
################################################################################
def resource_list_parser_function(input_files: SingleFile, groups: Dict[str, str]) -> List[str]:
    input_file = input_files["file"]
    calculator_page = groups["calculator_dir"]

    resource_cache_path = os.path.join("cache", calculator_page, "resources.pickle")
    page_metadata_path = os.path.join("cache", calculator_page, "page_metadata.json")

    errors: List[TokenError] = []

    resource_list: ResourceList

    resource_list, parse_errors = load_resource_list(input_file)
    errors += parse_errors

    resources: List[Resource] = [resource for resource in resource_list.resources if not isinstance(resource, Heading)]
    resources, expanding_raw_resource_errors = expand_raw_resource(resources)
    errors += expanding_raw_resource_errors
    resources = fill_default_requirement_groups(resources, resource_list.requirement_groups)

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
    os.makedirs(os.path.dirname(resource_cache_path), exist_ok=True)
    with open(resource_cache_path, 'wb') as f:
        pickle.dump(resource_list, f)

    os.makedirs(os.path.dirname(page_metadata_path), exist_ok=True)
    with open(page_metadata_path, 'w') as f:
        json.dump({
            "calculator_name": resource_list.index_page_display_name
        }, f)

    return [
        resource_cache_path,
        page_metadata_path,
    ]


def load_resource_list(filepath: str) -> Tuple[ResourceList, List[TokenError]]:
    errors: List[TokenError] = []

    with open(filepath, 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    return (resource_list, errors)


################################################################################
# expand_raw_resource
#
# expand_raw_resource allows for the syntactic candy of only defining a a
# `recipe_type` value for raw resources and not having to define the entire
# construct because it is a trivial construct.
################################################################################
def expand_raw_resource(resources: List[Resource]) -> Tuple[List[Resource], List[TokenError]]:
    errors: List[TokenError] = []
    for resource in resources:
        for recipe in resource.recipes:
            if recipe.recipe_type == "Raw Resource":
                # TODO: Have a better token associated with this error
                errors.append(TokenError(resource.name + " should not have a \"Raw Resource\". Instead use the raw_resource boolean on the resource itself", Token()))

        raw_resource_recipe = Recipe()
        raw_resource_recipe.recipe_type = "Raw Resource"
        raw_resource_recipe.output = 1
        raw_resource_recipe.requirements = OrderedDict([(resource.name, 0)])

        if resource.raw_resource:
            resource.recipes.insert(0, raw_resource_recipe)
        else:
            resource.recipes.append(raw_resource_recipe)

    return resources, errors


################################################################################
# fill_default_requirement_groups
#
# fill_default_requirement_groups replaces any uses of a requirement group with
# the first item within that requirement group. This is an interim solution
# while the requirement group feature is separately fleshed out. It has been
# included in this state because there is some simplicity value to being able
# to include the data structure in the resource_list.yaml file.
################################################################################
def fill_default_requirement_groups(resources: List[Resource], requirement_groups: OrderedDict[str, List[str]]) -> List[Resource]:
    for resource in resources:
        for recipe in resource.recipes:
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
    resources: List[Resource],
    recipe_types: OrderedDict[str, str],
    stack_sizes: OrderedDict[str, StackSize]
) -> List[TokenError]:
    errors: List[TokenError] = []
    for resource in resources:
        errors += lint_recipes(resource.name, resource.recipes)
        errors += lint_custom_stack_multipliers(resource.name, resource.custom_stack_multipliers, stack_sizes)

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
                errors.append(TokenError(item_name + " has an invalid \"Raw Resource\". You should use the resource.raw_resource boolean flag instead.", Token()))

    # Lint that every resource has a raw resource and only one
    if raw_resource_count == 0:
        # TODO: Have a better token associated with this error
        errors.append(TokenError(item_name + " must have a \"Raw Resource\". Use the resource.raw_resource boolean flag to indicate this.", Token()))
    elif raw_resource_count > 1:
        # TODO: Have a better token associated with this error
        errors.append(TokenError(item_name + " must have only one \"Raw Resource\". You should use the resource.raw_resource boolean flag instead.", Token()))

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
def ensure_valid_requirements(resources: List[Resource]) -> List[TokenError]:
    errors: List[TokenError] = []
    all_resource_names: Set[str] = set([x.name for x in resources])
    for resource in resources:
        for recipe in resource.recipes:
            for requirement in recipe.requirements:
                if requirement not in all_resource_names:
                    # TODO: Have a better token associated with this error
                    errors.append(TokenError("ERROR: Invalid requirement for resource:" + resource.name + ". \"" + requirement + "\" does not exist as a resource", Token()))
                elif recipe.requirements[requirement] < 0:
                    # TODO: Have a better token associated with this error
                    errors.append(TokenError("ERROR: Invalid requirement for resource:" + resource.name + ". \"" + requirement + "\" must be a positive number", Token()))
    return errors


################################################################################
# ensure_valid_recipe_types
#
# Validates that each defined recipe has a recipe type that exists.
################################################################################
def ensure_valid_recipe_types(resources: List[Resource], recipe_types: OrderedDict[str, str]) -> List[TokenError]:
    used_recipe_types: Set[str] = set()
    errors: List[TokenError] = []

    for resource in resources:
        for recipe in resource.recipes:
            recipe_type: str = recipe.recipe_type

            # add this to the list of found recipe types to later check to make sure all the recipe_types in the list are used
            if recipe_type != "Raw Resource":
                used_recipe_types.add(recipe_type)

            # check if this recipe exists in the recipe type list
            if recipe_type not in recipe_types and recipe_type != "Raw Resource":
                # TODO: Have a better token associated with this error
                errors.append(TokenError(resource.name + " has an undefined recipe_type" + ": \"" + recipe_type + "\"", Token()))

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
def ensure_unique_simple_names(resources: List[Resource]) -> List[TokenError]:
    errors: List[TokenError] = []
    simple_names: Dict[str, List[str]] = {}

    for resource in resources:
        simple_name: str = get_simple_name(resource)
        if simple_name not in simple_names:
            simple_names[simple_name] = []
        simple_names[simple_name].append(resource.name)

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
def get_simple_name(resource: Resource) -> str:
    # TODO: Change this if we end up implementing something like "is_set()" for the YAML conversions
    if resource.custom_simplename != "":
        return resource.custom_simplename
    return re.sub(r'[^a-z0-9]', '', resource.name.lower())
