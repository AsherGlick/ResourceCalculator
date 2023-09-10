from typing import Any, Dict, List, Union
from recipe_item import RecipeItem
from requirement_groups import ResourceGroups
import custom_recipes_shulker_box_coloring
import custom_recipes_fireworks



################################################################################
#
################################################################################
def parse_recipe_data(input_struct: Any, id_to_name_map: Dict[str, str], resource_groups: ResourceGroups) -> List[RecipeItem]:

    if "type" not in input_struct:
        raise ValueError("Cannot find recipe's type")

    if input_struct["type"] == "minecraft:crafting_shaped":
        return parse_shaped_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:crafting_shapeless":
        return parse_shapeless_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:smelting":
        return parse_smelting_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:blasting":
        return parse_blasting_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:smoking":
        return parse_smoking_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:smithing":
        return parse_smithing_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:campfire_cooking":
        return parse_campfire_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:stonecutting":
        return parse_stonecutting_data(input_struct, id_to_name_map, resource_groups)
    elif input_struct["type"] == "minecraft:smithing_transform":
        return parse_smithing_transform_data(input_struct, id_to_name_map, resource_groups)
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
    ]:
        return []
    else:
        raise ValueError("Unknown recipe 'type' {}".format(input_struct))


################################################################################
# parse_shaped_data
#
# Parses the data from recipes of the `minecraft:crafting_shaped` type.
################################################################################
def parse_shaped_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    confirm_keys(input_struct, ['key', 'pattern', 'result', 'type', 'category', 'show_notification'])

    count: int = 1
    if "count" in input_struct["result"]:
        count = input_struct["result"]["count"]
        del input_struct["result"]["count"]

    result = get_item_name_from_item_dict(input_struct["result"], id_to_name_map, resource_groups)



    # Sanity check that " " is an emtpy space for all recipe patterns
    if " " in input_struct["key"]:
        raise ValueError("Found ' ' as a key in a shaped recipe, it should be air and a null space")

    pattern = "".join(input_struct['pattern'])

    ingredients: Dict[str, int] = {}
    for character in pattern:
        if character == " ":
            continue

        itemdict = input_struct["key"][character]

        item_name = get_item_name_from_item_dict(itemdict, id_to_name_map, resource_groups)
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



def parse_shapeless_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    # We are going to ignore the "group" field that contains data about similar
    # recipes. EG: Deepslate Coal Ore and Coal Ore are both part of the Coal group
    if "group" in input_struct:
        del input_struct["group"]

    confirm_keys(input_struct, ['ingredients', 'result', 'type', 'category'])

    count: int = 1
    if "count" in input_struct["result"]:
        count = input_struct["result"]["count"]
        del input_struct["result"]["count"]

    result = get_item_name_from_item_dict(input_struct["result"], id_to_name_map, resource_groups)

    ingredients: Dict[str, int] = {}
    for ingredient in input_struct["ingredients"]:
        item_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)
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
def parse_campfire_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
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

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)

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
def parse_smoking_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
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

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)

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
def parse_blasting_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:

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

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)

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
def parse_smelting_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:

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

        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)

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
def parse_smithing_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    confirm_keys(input_struct, ['addition', 'base', 'result', 'type'])


    addition: str = get_item_name_from_item_dict(input_struct["addition"], id_to_name_map, resource_groups)
    base: str = get_item_name_from_item_dict(input_struct["base"], id_to_name_map, resource_groups)
    result: str = get_item_name_from_item_dict(input_struct["result"], id_to_name_map, resource_groups)

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
def parse_stonecutting_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    confirm_keys(input_struct, ['count', 'ingredient', 'result', 'type'])


    count:int = input_struct["count"]
    ingredient:str = get_item_name_from_item_dict(input_struct["ingredient"], id_to_name_map, resource_groups)
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


def parse_smithing_transform_data(
    input_struct: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    confirm_keys(input_struct, ['type', 'addition', 'base', 'result', 'template'])

    addition: str = get_item_name_from_item_dict(input_struct['addition'], id_to_name_map, resource_groups)
    base: str = get_item_name_from_item_dict(input_struct['base'], id_to_name_map, resource_groups)
    # template: str = get_item_name_from_item_dict(input_struct['template'], id_to_name_map, resource_groups) # TODO: templates are weird so we are ingoring them for now
    result: str = get_item_name_from_item_dict(input_struct["result"], id_to_name_map, resource_groups)

    return [
        RecipeItem(
            name=result,
            output=1,
            recipe_type="Smithing Table",
            requirements={
                base: 1,
                addition: 1,
            }
        )
    ]

################################################################################
################################################################################
################################################################################

# Helper function for unwrapping items
def get_item_name_from_item_dict(
    itemdict: Union[Dict[str, str], List[Dict[str,str]]],
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> str:
    # Sometimes the items that can be parsed are actually lists. This is a pretty
    # bad design decision on minecraft's part but it likely the result of legacy
    # code from a time before when they had item tags and they have not yet returned
    # to clean up all the recipes. We will do that for them, and tags that are
    # not present yet are manually created inside the resource_calculator_tag_groups
    # variable.
    if isinstance(itemdict, list):
        itemdict = get_tag_from_itemdict_list(itemdict, resource_groups)

    # We expect that the dict given to us at this point is a single element dict
    # containing the key "item" or "tag".
    if len(itemdict) > 1:
        raise ValueError("Itemdict should contain one key, either 'item' or 'tag'" + str(itemdict))

    if "tag" in itemdict:
        return resource_groups.get_display_name_from_group(itemdict["tag"])
    elif "item" in itemdict:
        return id_to_name_map[itemdict["item"]]

    raise ValueError("Itemdict should contain a key of either 'item' or 'tag' but contains neither" + str(itemdict))


def get_tag_from_itemdict_list(
    ingredient_list: List[Dict[str, str]],
    resource_groups: ResourceGroups
) -> Dict[str,str]:

    compact_list = sorted([x["item"] for x in ingredient_list])

    group_name = resource_groups.get_group_from_resources(compact_list)

    return {"tag": group_name}








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
