import sys

# Include the standard resource list parsing library
sys.path.append("../../../../")
from pylib.yaml_token_load import ordered_load
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, TokenError, Token, get_primitive

from io import BytesIO
from typing import Dict, Any, List, Set, Union
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

# A map between the minecraft tag names and the resource calculator resource
# goup names.


tagname_to_requirement_group: Dict[str, str] = {
    "minecraft:planks": "Any Planks",
    "minecraft:wooden_slabs": "Any Slab",
    "minecraft:logs": "Any Log",
    "minecraft:stone_crafting_materials": "Any Stone",
    "minecraft:sand": "Any Sand",
    "minecraft:logs_that_burn": "Any Log That Burns",
    "minecraft:acacia_logs": "Any Acacia Log",
    "minecraft:birch_logs": "Any Birch Log",
    "minecraft:crimson_stems": "Any Crimson Stem",
    "minecraft:dark_oak_logs": "Any Dark Oak Log",
    "minecraft:oak_logs": "Any Oak Log",
    "minecraft:jungle_logs": "Any Jungle Log",
    "minecraft:mangrove_logs": "Any Mangrove Log",
    "minecraft:spruce_logs": "Any Spruce Log",
    "minecraft:warped_stems": "Any Warped Stem",
    "minecraft:coals": "Any Coal",
    "minecraft:wool": "Any Wool",
    "minecraft:soul_fire_base_blocks": "Any Soul Fire Base Block",
    "minecraft:stone_tool_materials": "Any Stone Tool Material",
    "minecraft:shulker_boxes": "Any Shulker Box",

    # Corrisponding names for the custom resource_calculator_tag_groups
    "resourcecalculator:yellow_sandstone": "Any Yellow Sandstone",
    "resourcecalculator:uncut_yellow_sandstone": "Any Uncut Yellow Sandstone",
    "resourcecalculator:red_sandstone": "Any Red Sandstone",
    "resourcecalculator:uncut_red_sandstone": "Any Uncut Red Sandstone",
    "resourcecalculator:unsmooth_quartz_block": "Any Unsmooth Quartz Block",
    "resourcecalculator:purpur_block": "Any Purpur Block",
}

requirement_group_to_tagname: Dict[str, str] = { v:k for k, v in tagname_to_requirement_group.items() }

# Additional groups that are not defined by minecraft but defined instead using
# the array schema where an item's resource is an array of items instead of
# a single one, indicating any of those items may be used. This is added to
# all_tags in the get_all_tags() function.
resource_calculator_tag_groups: Dict[str, List[str]] = {
    "resourcecalculator:yellow_sandstone": [
        'minecraft:chiseled_sandstone',
        'minecraft:cut_sandstone',
        'minecraft:sandstone',
    ],
    "resourcecalculator:uncut_yellow_sandstone": [
        'minecraft:chiseled_sandstone',
        'minecraft:sandstone',
    ],

    "resourcecalculator:red_sandstone": [
        'minecraft:chiseled_red_sandstone',
        'minecraft:cut_red_sandstone',
        'minecraft:red_sandstone',
    ],

    "resourcecalculator:uncut_red_sandstone": [
        'minecraft:chiseled_red_sandstone',
        'minecraft:red_sandstone',
    ],

    "resourcecalculator:unsmooth_quartz_block": [
        'minecraft:chiseled_quartz_block',
        'minecraft:quartz_block',
        'minecraft:quartz_pillar',
    ],

    "resourcecalculator:purpur_block": [
        'minecraft:purpur_block',
        'minecraft:purpur_pillar',
    ]
}


all_tags: Dict[str, List[str]] = {}
id_to_name_map: Dict[str, str] = {}




################################################################################
# Parse all of the tagfiles
################################################################################
def get_all_tags(jarfile: zipfile.ZipFile) -> Dict[str, List[str]]:
    all_tags: Dict[str, List[str]] = {}

    file_list = jarfile.infolist()
    for file in file_list:
        filename = file.filename

        if filename.startswith("data/minecraft/tags/blocks") \
            or filename.startswith("data/minecraft/tags/items"):
                key = os.path.splitext(os.path.basename(filename))[0]

                all_tags["minecraft:"+key] = sorted(list(set(parse_tagfile(jarfile, filename))))

    for tag in resource_calculator_tag_groups:
        all_tags[tag] = resource_calculator_tag_groups[tag]

    return all_tags


################################################################################
# Parse a given tag file. Tag files contain the equivlent of requirement groups
# and may be nested to contain other tagfiles. If a file contains another nested
# file then recursively open that file and add its contents to this tag.
################################################################################
def parse_tagfile(jarfile: zipfile.ZipFile, tag_filename: str) -> List[str]:
    tags: List[str] = []

    files = set([x.filename for x in jarfile.infolist()])

    tagfile_data = json.load(BytesIO(jarfile.read(tag_filename)))

    assert(len(tagfile_data) == 1)
    assert("values" in tagfile_data)
    assert(type(tagfile_data["values"] == list))

    for tag in tagfile_data["values"]:
        assert(type(tag) == str)

        if tag.startswith("#"):
            blocksfile = "data/minecraft/tags/blocks/" + tag[11:] + ".json"
            itemsfile = "data/minecraft/tags/items/" + tag[11:] + ".json"

            if blocksfile in files:
                tags += parse_tagfile(jarfile, blocksfile)
            elif itemsfile in files:
                tags += parse_tagfile(jarfile, itemsfile)

        else:
            tags.append(tag)

    return tags

def main() -> None:
    jar_location = sys.argv[1]

    zipped_file = zipfile.ZipFile(jar_location, 'r')

    global id_to_name_map
    id_to_name_map = get_item_id_translations(zipped_file)

    global all_tags
    all_tags = get_all_tags(zipped_file)


    # Build the recipe list from all of the recipe objects in the jar.
    recipes:List[RecipeItem] = []
    try:
        file_list = zipped_file.infolist()
        for zipped_item in file_list:
            filename = zipped_item.filename

            if not filename.startswith("data/minecraft/recipes"):
                continue

            recipe_data = BytesIO(zipped_file.read(filename))

            recipes += parse_recipe_data(json.load(recipe_data), id_to_name_map)

    finally:
        zipped_file.close()

    # Add any custom recipes that are not included in the jar.
    recipes += custom_recipes_carving.recipes()
    recipes += custom_recipes_stripping.recipes([id_to_name_map[x] for x in all_tags["minecraft:logs"]])
    recipes += custom_recipes_tilling.recipes()
    recipes += custom_recipes_shoveling.recipes()
    recipes += custom_recipes_water.recipes()
    recipes += custom_recipes_oxidation.recipes()

    # Calculate all of the used tags/requirement groups.
    used_tags: Set[str] = set([])
    for recipe in recipes:
        for requirement in recipe.requirements:
            if requirement in requirement_group_to_tagname:
                used_tags.add(requirement_group_to_tagname[requirement])

    # Build the contents of each used requirement group.
    groups: Dict[str, List[str]] = {}
    for tag in used_tags:
        groups[tag] = all_tags[tag]

    # Validate the `resources.yaml` file against the data parsed.
    validate_resources(recipes, groups)


def get_tag_from_itemdict_list(ingredient_list: List[Dict[str, str]]) -> Dict[str,str]:

    compact_list = sorted([x["item"] for x in ingredient_list])

    for tag, value in all_tags.items():
        if value == compact_list:
            return {"tag": tag}

    raise ValueError("No matching tag for" + str(compact_list))



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
    ]:
        return []
    else:
        raise ValueError(input_struct)



def parse_shaped_data(input_struct: Any, id_to_name_map: Dict[str, str]) -> List[RecipeItem]:
    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    assert(sorted(input_struct.keys()) == ['key', 'pattern', 'result', 'type'])

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

    assert(sorted(input_struct.keys()) == ['ingredients', 'result', 'type'])

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

    assert(sorted(input_struct.keys()) == ['cookingtime', 'ingredient', 'result', 'type'])

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

    assert(sorted(input_struct.keys()) == ['cookingtime', 'ingredient', 'result', 'type'])

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

    assert(sorted(input_struct.keys()) == ['cookingtime', 'ingredient', 'result', 'type'])

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

    assert(sorted(input_struct.keys()) == ['cookingtime', 'ingredient', 'result', 'type'])

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
    assert(sorted(input_struct.keys()) == ['addition', 'base', 'result', 'type'])

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
    assert(sorted(input_struct.keys()) == ['count', 'ingredient', 'result', 'type'])

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
        return tagname_to_requirement_group[itemdict["tag"]]
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
def validate_resources(recipes:List[RecipeItem], groups: Dict[str, List[str]]) -> None:

    errors: List[TokenError] = []
    with open("../../resources.yaml", 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    validate_recipes(recipes, resource_list.resources)
    validate_requirement_groups(groups, resource_list.requirement_groups)


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
    resource_requirement_groups:Dict[str, List[str]]
) -> None:
    output = {}

    for group in sorted(groups.keys()):
        output[tagname_to_requirement_group[group]] = [id_to_name_map[x] for x in groups[group]]

    # Validate all groups are requirement groups
    for group in output:
        if group not in resource_requirement_groups:
            print("Missing Requirement Group")
            print(yaml.dump({group:output[group]}))

        for item in output[group]:
            if item not in resource_requirement_groups[group]:
                print("Requirement Group has incorrect elements. Should be:")
                print(yaml.dump({group:output[group]}))

    # Validate all requirement groups are groups
    for group in resource_requirement_groups:
        if group not in output:
            print("Extra Requirement Group Found")
            print(yaml.dump({group:resource_requirement_groups[group]}))

main()
