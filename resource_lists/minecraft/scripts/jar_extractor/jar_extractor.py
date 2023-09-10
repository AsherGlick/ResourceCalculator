################################################################################
# python3 jar_extractor.py ~/.minecraft/versions/1.20.1/1.20.1.jar
#
#
################################################################################

import sys

# Include the standard resource list parsing library
sys.path.append("../../../../")
from pylib.yaml_token_load import ordered_load
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, TokenError, Token, get_primitive

from io import BytesIO
from typing import Dict, Any, List, Set, Union, TypedDict
import json
import os
import re
import zipfile
import yaml
from recipe_item import RecipeItem
import custom_recipes_carving
import custom_recipes_stripping
import custom_recipes_tilling
import custom_recipes_shoveling
import custom_recipes_water
import custom_recipes_oxidation
from requirement_groups import ResourceGroups
from recipe_parser import parse_recipe_data


SKIPPED_RECIPES: Set[str] = set([
    "data/minecraft/recipes/coast_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/dune_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/eye_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/host_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/netherite_upgrade_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/raiser_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/rib_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/sentry_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/shaper_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/silence_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/snout_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/spire_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/tide_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/vex_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/ward_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/wayfinder_armor_trim_smithing_template.json", # Recursive Recipe
    "data/minecraft/recipes/wild_armor_trim_smithing_template.json", # Recursive Recipe
])

resource_groups: ResourceGroups

def main() -> None:
    jar_location = sys.argv[1]

    zipped_file = zipfile.ZipFile(jar_location, 'r')

    id_to_name_map = get_item_id_translations(zipped_file)

    global resource_groups
    resource_groups = ResourceGroups(zipped_file, id_to_name_map)

    # Build the recipe list from all of the recipe objects in the jar.
    recipes:List[RecipeItem] = []
    try:
        file_list = zipped_file.infolist()
        for zipped_item in file_list:
            filename = zipped_item.filename

            if not filename.startswith("data/minecraft/recipes"):
                continue

            if filename in SKIPPED_RECIPES:
                continue

            recipe_data = BytesIO(zipped_file.read(filename))

            recipes += parse_recipe_data(json.load(recipe_data), id_to_name_map, resource_groups)

    finally:
        zipped_file.close()

    # Add any custom recipes that are not included in the jar.
    recipes += custom_recipes_carving.recipes()
    recipes += custom_recipes_stripping.recipes([id_to_name_map[x] for x in resource_groups.get_resouces_from_group("minecraft:logs")])
    recipes += custom_recipes_tilling.recipes()
    recipes += custom_recipes_shoveling.recipes()
    recipes += custom_recipes_water.recipes()
    recipes += custom_recipes_oxidation.recipes()

    # Calculate and deduplicate all of the used tags/requirement groups.
    used_tags: Set[str] = set([])
    for recipe in recipes:
        for requirement in recipe.requirements:
            if resource_groups.is_display_name_a_group(requirement):
                used_tags.add(resource_groups.get_group_from_display_name(requirement))

    # Build the contents of each used requirement group.
    groups: Dict[str, List[str]] = {}
    for tag in used_tags:
        groups[tag] = resource_groups.get_resouces_from_group(tag)

    # Validate the `resources.yaml` file against the data parsed.
    validate_resources(recipes, groups, id_to_name_map)


################################################################################
# Get the item id's names by looking at the english us translation table. All
# of the items inside the resource calculator are in english so we need these
# values in order to match up the recipes to them.
################################################################################
def get_item_id_translations(jarfile: zipfile.ZipFile) -> Dict[str, str]:

    block_tn_prefix = "block.minecraft."
    item_tn_prefix = "item.minecraft."
    id_prefix = "minecraft:"
    translations = json.load(BytesIO(jarfile.read("assets/minecraft/lang/en_us.json")))


    item_id_translations: Dict[str, str] = {}
    for key, value in translations.items():
        if re.match("^" + block_tn_prefix + "[a-z_0-9]+$", key):
            item_id_translations[key.replace(block_tn_prefix, id_prefix)] = value

        elif re.match("^" + item_tn_prefix + "[a-z_0-9]+$", key):
            item_id_translations[key.replace(item_tn_prefix, id_prefix)] = value

    return item_id_translations





################################################################################
############################### Recipe Validation ##############################
################################################################################

################################################################################
# validate_resources
#
# Validates that multiple aspects of the resources.yaml file are correct.
################################################################################
def validate_resources(recipes:List[RecipeItem], groups: Dict[str, List[str]], id_to_name_map: Dict[str, str]) -> None:

    errors: List[TokenError] = []
    with open("../../resources.yaml", 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    validate_recipes(recipes, resource_list.resources)
    validate_requirement_groups(groups, resource_list.requirement_groups, id_to_name_map)


################################################################################
# print_recipee_yaml
#
# A helper function for converting a RecipeItem into a yaml output
################################################################################
def print_recipe_yaml(recipe: RecipeItem) -> None:
    print("    - output: " + str(recipe.output))
    print("      recipe_type: " + recipe.recipe_type)
    print("      requirements:")
    for requirement in recipe.requirements:
        print("        " + requirement + ": " + str(- recipe.requirements[requirement]))


################################################################################
# is_matching_recipe
#
# A helper function for comparing recipes to see if they are the same or not
################################################################################
def is_matching_recipe(jar_recipe: RecipeItem, resource_recipe: Recipe) -> bool:
    if jar_recipe.output != resource_recipe.output:
        return False
    
    if jar_recipe.recipe_type != resource_recipe.recipe_type:
        return False


    for requirement in jar_recipe.requirements:
        if requirement not in resource_recipe.requirements:
            return False

        if jar_recipe.requirements[requirement] != -resource_recipe.requirements[requirement]:
            return False

    for requirement in resource_recipe.requirements:
        if requirement not in jar_recipe.requirements:
            return False

        if jar_recipe.requirements[requirement] != -resource_recipe.requirements[requirement]:
            return False

    return True

################################################################################
# validate_recipes
#
# Validate that all of the recipes parsed from the jar file are stored in the
# resources.yaml file and make sure that all of the recipes in the resources.yaml
# file are one that have been parsed from the jar file.
################################################################################
def validate_recipes(jar_recipes: List[RecipeItem], resource_recipes: Dict[str, Resource]) -> None:

    # Validate all jar recipes are in the resource recipes
    for jar_recipe in jar_recipes:
        if jar_recipe.name not in resource_recipes:
            print("Cannot find recipes for", jar_recipe.name)
            print("Expecting")
            print("  " + jar_recipe.name + ":")
            print("    recipes:")
            print_recipe_yaml(jar_recipe)
            print("    - recipe_type: Raw Resource")

            print("")
            continue

        item_resource_recipes: List[Recipe] = resource_recipes[jar_recipe.name].recipes

        has_matching_recipe = False
        for resource_recipe in item_resource_recipes:
            if is_matching_recipe(jar_recipe, resource_recipe):
                has_matching_recipe = True
                break

        if not has_matching_recipe:
            print("YAML Missing Recipe for \"" +jar_recipe.name + "\"")
            print_recipe_yaml(jar_recipe)
            continue

    # Validate all resource recipes are in jar recipes
    for resource in resource_recipes:

        # Ignore our custom resource of fuel
        if resource == "Fuel":
            continue

        for resource_recipe in resource_recipes[resource].recipes:
            if resource_recipe.recipe_type == "Raw Resource":
                continue

            has_matching_recipe = False
            for jar_recipe in jar_recipes:
                if jar_recipe.name == resource and is_matching_recipe(jar_recipe, resource_recipe):
                    has_matching_recipe = True
                    break

            if not has_matching_recipe:
                print("Found Extra Yaml Recipe \""+resource+"\"")
                print(resource_recipe.to_yaml())


################################################################################
# validate_requirement_groups
#
# Validate that the requirement groups inside the resources.yaml file are
# all correct and that all of the generated resource groups are present.
################################################################################
def validate_requirement_groups(
    groups: Dict[str, List[str]],
    resource_requirement_groups:Dict[str, List[str]],
    id_to_name_map: Dict[str, str],
) -> None:
    output = {}

    for group in sorted(groups.keys()):
        output[resource_groups.get_display_name_from_group(group)] = [id_to_name_map[x] for x in groups[group]]

    # Validate all groups are requirement groups
    for group in output:
        if group not in resource_requirement_groups:
            print("Missing Requirement Group")
            print(yaml.dump({group:output[group]}))

        else:
            for item in output[group]:
                if item not in resource_requirement_groups[group]:
                    print("Requirement Group has incorrect elements. Should be:")
                    print(yaml.dump({group:output[group]}))
                    # This prints for every item that is missing from the YAML
            # TODO: Check that nothing in the yaml should no longer be there


    # Validate all requirement groups are groups
    for group in resource_requirement_groups:
        if group not in output:
            print("Extra Requirement Group Found")
            print(yaml.dump({group:resource_requirement_groups[group]}))

main()
