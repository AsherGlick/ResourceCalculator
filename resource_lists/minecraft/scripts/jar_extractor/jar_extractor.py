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
import custom_recipes_shulker_box_coloring
import custom_recipes_fireworks
import custom_recipes_oxidation
from requirement_groups import ResourceGroups


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
    resource_groups = ResourceGroups(zipped_file)


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

            recipes += parse_recipe_data(json.load(recipe_data), id_to_name_map)

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
# confirm_keys
#
# A helper function to confirm that specific keys are in a dictionary and that
# unknown keys are not in the dictionary. Displaying helpful error messages
# if the dictionary is incorrect.
################################################################################
def confirm_keys(obj: Dict[str, Any], required_keys: List[str], optional_keys: List[str] = []) -> None:
    for required_key in required_keys:
        if required_key not in obj:
            raise ValueError("{} is not found in {}".format(required_key, obj))

    allowed_keys = set(required_keys + optional_keys)
    for present_key in obj.keys():
        if present_key not in allowed_keys:
            raise ValueError("{} should not be in {}".format(present_key, obj))


def get_tag_from_itemdict_list(ingredient_list: List[Dict[str, str]]) -> Dict[str,str]:

    compact_list = sorted([x["item"] for x in ingredient_list])

    group_name = resource_groups.get_group_from_resources(compact_list)

    return {"tag": group_name}



def parse_recipe_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:

    if "type" not in input_struct:
        raise ValueError("Cannot find recipe's type")

    if input_struct["type"] == "minecraft:crafting_shaped":
        return parse_shaped_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:crafting_shapeless":
        return parse_shapeless_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:smelting":
        return parse_smelting_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:blasting":
        return parse_blasting_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:smoking":
        return parse_smoking_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:smithing":
        return parse_smithing_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:campfire_cooking":
        return parse_campfire_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:stonecutting":
        return parse_stonecutting_data(input_struct, id_to_name_map)
    elif input_struct["type"] == "minecraft:crafting_special_shulkerboxcoloring":
        return custom_recipes_shulker_box_coloring.recipes()
    elif input_struct["type"] == "minecraft:crafting_special_firework_rocket":
        return custom_recipes_fireworks.recipes()
    elif input_struct["type"] in [
        "minecraft:crafting_special_armordye",
        "minecraft:crafting_special_bannerduplicate",
        "minecraft:crafting_special_bookcloning",
        "minecraft:crafting_special_firework_star",
        "minecraft:crafting_special_firework_star_fade",
        "minecraft:crafting_special_mapcloning",
        "minecraft:crafting_special_mapextending",
        "minecraft:crafting_special_repairitem",
        "minecraft:crafting_special_shielddecoration",
        "minecraft:crafting_special_suspiciousstew",
        "minecraft:crafting_special_tippedarrow",
        "minecraft:smithing_trim",
        "minecraft:crafting_decorated_pot",

        "minecraft:smithing_transform", # TODO: this should probably actually be implemented
    ]:
        return []
    else:
        raise ValueError("Unknown recipe 'type' {}".format(input_struct))



################################################################################
# parse_shaped_data
#
# Parses the data from recipes of the `minecraft:crafting_shaped` type.
################################################################################
def parse_shaped_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:
    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    confirm_keys(input_struct, ['key', 'pattern', 'result', 'type', 'category', 'show_notification'])

    count: int = 1
    if "count" in input_struct["result"]:
        count = input_struct["result"]["count"]
        del input_struct["result"]["count"]

    result = get_item_name_from_item_dict(input_struct["result"], id_to_name_map)



    # Sanity check that " " is an emtpy space for all recipe patterns
    if " " in input_struct["key"]:
        raise ValueError("Found ' ' as a key in a shaped recipe, it should be air and a null space")

    pattern = "".join(input_struct['pattern'])

    ingredients: Dict[str, int] = {}
    for character in pattern:
        if character == " ":
            continue

        itemdict = input_struct["key"][character]

        item_name = get_item_name_from_item_dict(itemdict, id_to_name_map)
        if item_name not in ingredients:
            ingredients[item_name] = 0

        ingredients[item_name] += 1

    recipe_item = RecipeItem(
        name=result,
        output=count,
        recipe_type="Crafting",
        requirements=ingredients
    )


    return [recipe_item]



def parse_shapeless_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:
    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    confirm_keys(input_struct, ['ingredients', 'result', 'type', 'category'])

    count: int = 1
    if "count" in input_struct["result"]:
        count = input_struct["result"]["count"]
        del input_struct["result"]["count"]

    result = get_item_name_from_item_dict(input_struct["result"], id_to_name_map)

    ingredients: Dict[str, int] = {}
    for ingredient in input_struct["ingredients"]:
        item_name = get_item_name_from_item_dict(ingredient, id_to_name_map)
        if item_name not in ingredients:
            ingredients[item_name] = 0

        ingredients[item_name] += 1


    recipe_item = RecipeItem(
        name=result,
        output=count,
        recipe_type="Crafting",
        requirements=ingredients
    )


    return [recipe_item]





# TODO: Figure out how to merge these into the regular recipe list
def parse_campfire_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:
    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    # We are going to ignore the "experience" field that indicates how much exp
    # the player is awarded via crafting.
    if "experience" in input_struct:
        del input_struct["experience"]

    confirm_keys(input_struct, ['cookingtime', 'ingredient', 'result', 'type', 'category'])

    cooking_time = input_struct["cookingtime"]
    if cooking_time != 600:
        raise ValueError("Non 600 cooking time, a feature is needed to convert this value into a correct fuel value")

    result: str = input_struct["result"]
    ingredients = input_struct["ingredient"]

    # Convert any single values into a single element list to take avantage of
    # common processing
    if type(ingredients) == dict:
        ingredients = [ingredients]

    recipe_items: List[RecipeItem] = []

    for ingredient in ingredients:

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map)

        recipe_items.append(RecipeItem(
            name=id_to_name_map[result],
            output=1,
            recipe_type="Campfire",
            requirements={
                ingredient_name : 1
            }
        ))

    # TODO: Hold off of sending Campfire Recipes just yet because they might all
    # be exactly the same as smelting recipes but just for food and not require coal.
    return [] #recipe_items

# TODO: Figure out how to merge these into the regular recipe list
def parse_smoking_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:
    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    # We are going to ignore the "experience" field that indicates how much exp
    # the player is awarded via crafting.
    if "experience" in input_struct:
        del input_struct["experience"]

    confirm_keys(input_struct, ['cookingtime', 'ingredient', 'result', 'type', 'category'])

    cooking_time = input_struct["cookingtime"]
    if cooking_time != 100:
        raise ValueError("Non 100 cooking time, a feature is needed to convert this value into a correct fuel value")

    result: str = input_struct["result"]
    ingredients = input_struct["ingredient"]

    # Convert any single values into a single element list to take avantage of
    # common processing
    if type(ingredients) == dict:
        ingredients = [ingredients]

    recipe_items: List[RecipeItem] = []

    for ingredient in ingredients:

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map)

        recipe_items.append(RecipeItem(
            name=id_to_name_map[result],
            output=1,
            recipe_type="Smoking",
            requirements={
                ingredient_name : 1
            }
        ))

    # TODO: Hold off of sending Smoking Recipes just yet because they might all
    # be exactly the same as smelting recipes but just for food.
    return [] #recipe_items


# TODO: Figure out how to merge these into the regular recipe list
def parse_blasting_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:

    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    # We are going to ignore the "experience" field that indicates how much exp
    # the player is awarded via crafting.
    if "experience" in input_struct:
        del input_struct["experience"]

    confirm_keys(input_struct, ['cookingtime', 'ingredient', 'result', 'type', 'category'])

    cooking_time = input_struct["cookingtime"]
    if cooking_time != 100:
        raise ValueError("Non 100 cooking time, a feature is needed to convert this value into a correct fuel value")

    result: str = input_struct["result"]
    ingredients = input_struct["ingredient"]

    # Convert any single values into a single element list to take avantage of
    # common processing
    if type(ingredients) == dict:
        ingredients = [ingredients]

    recipe_items: List[RecipeItem] = []

    for ingredient in ingredients:

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map)

        recipe_items.append(RecipeItem(
            name=id_to_name_map[result],
            output=1,
            recipe_type="Blasting",
            requirements={
                ingredient_name : 1,
                "Fuel": 1,
            }
        ))

    # TODO: Hold off of sending Blasting Recipes just yet because they might all
    # be exactly the same as smelting but just for ores/stones/etc recipes.
    return [] #recipe_items

################################################################################
# Parse the Smelting Recipes
################################################################################
def parse_smelting_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:

    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    # We are going to ignore the "experience" field that indicates how much exp
    # the player is awarded via crafting.
    if "experience" in input_struct:
        del input_struct["experience"]

    confirm_keys(input_struct, ['cookingtime', 'ingredient', 'result', 'type', 'category'])

    cooking_time = input_struct["cookingtime"]
    if cooking_time != 200:
        raise ValueError("Non 200 cooking time, a feature is needed to convert this value into a correct fuel value")

    result: str = input_struct["result"]
    ingredients = input_struct["ingredient"]

    # Convert any single values into a single element list to take avantage of
    # common processing
    if type(ingredients) == dict:
        ingredients = [ingredients]

    recipe_items: List[RecipeItem] = []

    for ingredient in ingredients:

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map)

        recipe_items.append(RecipeItem(
            name=id_to_name_map[result],
            output=1,
            recipe_type="Smelting",
            requirements={
                ingredient_name : 1,
                "Fuel": 1,
            }
        ))

    return recipe_items


# Parse the anvil recipe types into a recipe item
def parse_smithing_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:
    confirm_keys(input_struct, ['addition', 'base', 'result', 'type'])


    addition: str = get_item_name_from_item_dict(input_struct["addition"], id_to_name_map)
    base: str = get_item_name_from_item_dict(input_struct["base"], id_to_name_map)
    result: str = get_item_name_from_item_dict(input_struct["result"], id_to_name_map)

    recipe_item = RecipeItem(
        name=result,
        output=1,
        recipe_type="Smithing Table",
        requirements={
            base : 1,
            addition : 1,
        }
    )

    return [recipe_item]

################################################################################
# Parse the stonecutting recipe type into a recipe item
################################################################################
def parse_stonecutting_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:
    confirm_keys(input_struct, ['count', 'ingredient', 'result', 'type'])


    count:int = input_struct["count"]
    ingredient:str = get_item_name_from_item_dict(input_struct["ingredient"], id_to_name_map)
    result: str = input_struct["result"]

    recipe_item = RecipeItem(
        name=id_to_name_map[result],
        output=count,
        recipe_type="Cutting",
        requirements={
            ingredient : 1
        }
    )
    return [recipe_item]


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


# Helper function for unwrapping items
def get_item_name_from_item_dict(itemdict: Union[Dict[str, str], List[Dict[str,str]]], id_to_name_map: Dict[str, str]) -> str:
    # Sometimes the items that can be parsed are actually lists. This is a pretty
    # bad design decision on minecraft's part but it likely the result of legacy
    # code from a time before when they had item tags and they have not yet returned
    # to clean up all the recipes. We will do that for them, and tags that are
    # not present yet are manually created inside the resource_calculator_tag_groups
    # variable.
    if isinstance(itemdict, list):
        itemdict = get_tag_from_itemdict_list(itemdict)

    # We expect that the dict given to us at this point is a single element dict
    # containing the key "item" or "tag".
    if len(itemdict) > 1:
        raise ValueError("Itemdict should contain one key, either 'item' or 'tag'" + str(itemdict))

    if "tag" in itemdict:
        return resource_groups.get_display_name_from_group(itemdict["tag"])
    elif "item" in itemdict:
        return id_to_name_map[itemdict["item"]]

    raise ValueError("Itemdict should contain a key of either 'item' or 'tag' but contains neither" + str(itemdict))



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
