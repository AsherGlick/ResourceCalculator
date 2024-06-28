from typing import Any, Dict, List, Union, Literal, Optional
from recipe_item import RecipeItem
from requirement_groups import ResourceGroups
import custom_recipes_shulker_box_coloring
import custom_recipes_fireworks
from dataclasses import dataclass, field
import classnotation


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

@dataclass
class Result:
    item_id: str = field(metadata={"json": "id"})
    count: int = 1

@dataclass
class ItemDictItem:
    item: str

@dataclass
class ItemDictTag:
    tag: str

ItemDict = Union[ItemDictItem, ItemDictTag, List[ItemDictItem]]

################################################################################
################################ Shaped Recipes ################################
################################################################################
@dataclass
class ShapedData:
    recipe_type: Literal["minecraft:crafting_shaped"] = field(metadata={"json": "type"})
    category: str
    key: Dict[str, ItemDict]
    pattern: List[str]
    result: Result
    group: Optional[str] = None
    show_notification: Optional[bool] = None


################################################################################
# parse_shaped_data
#
# Parses the data from recipes of the `minecraft:crafting_shaped` type.
################################################################################
def parse_shaped_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    input_struct: ShapedData = classnotation.load_data(ShapedData, input_data)

    # result = get_item_name_from_item_dict(input_struct["result"], id_to_name_map, resource_groups)
    result = id_to_name_map[input_struct.result.item_id]

    # Sanity check that " " is an emtpy space for all recipe patterns
    if " " in input_struct.key:
        raise ValueError("Found ' ' as a key in a shaped recipe, it should be air and a null space")

    pattern: str = "".join(input_struct.pattern)

    ingredients: Dict[str, int] = {}
    for character in pattern:
        if character == " ":
            continue

        itemdict = input_struct.key[character]

        item_name = get_item_name_from_item_dict(itemdict, id_to_name_map, resource_groups)
        if item_name not in ingredients:
            ingredients[item_name] = 0

        ingredients[item_name] += 1

    recipe_item = RecipeItem(
        name=result,
        output=input_struct.result.count,
        recipe_type="Crafting",
        requirements=ingredients
    )


    return [recipe_item]


################################################################################
############################## Shapeless Recipes ###############################
################################################################################
@dataclass
class ShapelessData:
    recipe_type: Literal["minecraft:crafting_shapeless"] = field(metadata={"json": "type"})
    category: str
    ingredients: List[ItemDict]
    result: Result
    group: Optional[str] = None


def parse_shapeless_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    input_struct: ShapelessData = classnotation.load_data(ShapelessData, input_data)

    # result = get_item_name_from_item_dict(input_struct["result"], id_to_name_map, resource_groups)
    result = id_to_name_map[input_struct.result.item_id]

    ingredients: Dict[str, int] = {}
    for ingredient in input_struct.ingredients:
        item_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)
        if item_name not in ingredients:
            ingredients[item_name] = 0

        ingredients[item_name] += 1


    recipe_item = RecipeItem(
        name=result,
        output=input_struct.result.count,
        recipe_type="Crafting",
        requirements=ingredients
    )

    return [recipe_item]


################################################################################
############################### Campfire Recipes ###############################
################################################################################
# TODO: Figure out how to merge these into the regular recipe list
@dataclass
class CampfireData:
    item_type: Literal["minecraft:campfire_cooking"] = field(metadata={"json": "type"})
    category: str
    cookingtime: int
    experience: float
    ingredient: ItemDict
    result: Result


def parse_campfire_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    input_struct = classnotation.load_data(CampfireData, input_data)

    if input_struct.cookingtime != 600:
        raise ValueError("Non 600 cooking time, a feature is needed to convert this value into a correct fuel value")

    ingredients = [input_struct.ingredient]

    recipe_items: List[RecipeItem] = []

    for ingredient in ingredients:
        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)

        recipe_items.append(RecipeItem(
            name=id_to_name_map[input_struct.result.item_id],
            output=input_struct.result.count,
            recipe_type="Campfire",
            requirements={
                ingredient_name : 1
            }
        ))

    # TODO: Hold off of sending Campfire Recipes just yet because they might all
    # be exactly the same as smelting recipes but just for food and not require coal.
    return [] #recipe_items


################################################################################
############################### Smoking Recipes ################################
################################################################################
@dataclass
class SmokingData:
    item_type: Literal["minecraft:smoking"] = field(metadata={"json": "type"})
    category: str
    cookingtime: int
    experience: float
    ingredient: ItemDict
    result: Result


# TODO: Figure out how to merge these into the regular recipe list
def parse_smoking_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    input_struct = classnotation.load_data(SmokingData, input_data)

    if input_struct.cookingtime != 100:
        raise ValueError("Non 100 cooking time, a feature is needed to convert this value into a correct fuel value")

    # Hack to unwrap lists of itemdicts into individual recipes to avoid making
    # custom groups for singleinput recipes.
    ingredients = input_struct.ingredient
    if isinstance(ingredients, ItemDictItem) or isinstance(ingredients, ItemDictTag):
        ingredients = [ingredients]

    recipe_items: List[RecipeItem] = []

    for ingredient in ingredients:
        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)
        recipe_items.append(RecipeItem(
            name=id_to_name_map[input_struct.result.item_id],
            output=input_struct.result.count,
            recipe_type="Smoking",
            requirements={
                ingredient_name : 1
            }
        ))

    # TODO: Hold off of sending Smoking Recipes just yet because they might all
    # be exactly the same as smelting recipes but just for food.
    return [] #recipe_items


################################################################################
############################### Blasting Recipes ###############################
################################################################################
@dataclass
class BlastingData:
    item_type: Literal["minecraft:blasting"] = field(metadata={"json": "type"})
    category: str
    cookingtime: int
    experience: float
    ingredient: ItemDict
    result: Result
    group: Optional[str] = None


# TODO: Figure out how to merge these into the regular recipe list
def parse_blasting_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:

    input_struct = classnotation.load_data(BlastingData, input_data)

    if input_struct.cookingtime != 100:
        raise ValueError("Non 100 cooking time, a feature is needed to convert this value into a correct fuel value")

    # Hack to unwrap lists of itemdicts into individual recipes to avoid making
    # custom groups for singleinput recipes.
    ingredients = input_struct.ingredient
    if isinstance(ingredients, ItemDictItem) or isinstance(ingredients, ItemDictTag):
        ingredients = [ingredients]

    recipe_items: List[RecipeItem] = []
    for ingredient in ingredients:
        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)
        recipe_items.append(RecipeItem(
            name=id_to_name_map[input_struct.result.item_id],
            output=input_struct.result.count,
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
@dataclass
class SmeltingData:
    item_type: Literal["minecraft:smelting"] = field(metadata={"json": "type"})
    category: str
    cookingtime: int
    experience: float
    ingredient: ItemDict
    result: Result
    group: Optional[str] = None

def parse_smelting_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    input_struct = classnotation.load_data(SmeltingData, input_data)

    # Sanity check cooing time
    if input_struct.cookingtime != 200:
        raise ValueError("Non 200 cooking time, a feature is needed to convert this value into a correct fuel value")

    # Hack to unwrap lists of itemdicts into individual recipes to avoid making
    # custom groups for singleinput recipes.
    ingredients = input_struct.ingredient
    if isinstance(ingredients, ItemDictItem) or isinstance(ingredients, ItemDictTag):
        ingredients = [ingredients]

    recipe_items: List[RecipeItem] = []
    for ingredient in ingredients:
        ingredient_name = get_item_name_from_item_dict(ingredient, id_to_name_map, resource_groups)
        recipe_items.append(RecipeItem(
            name=id_to_name_map[input_struct.result.item_id],
            output=input_struct.result.count,
            recipe_type="Smelting",
            requirements={
                ingredient_name : 1,
                "Fuel": 1,
            }
        ))

    return recipe_items



################################################################################
# Parse the stonecutting recipe type into a recipe item
################################################################################
@dataclass
class StonecuttingData:
    recipe_type: Literal["minecraft:stonecutting"] = field(metadata={"json": "type"})
    ingredient: ItemDict
    result: Result

def parse_stonecutting_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    input_struct = classnotation.load_data(StonecuttingData, input_data)

    ingredient:str = get_item_name_from_item_dict(
        input_struct.ingredient,
        id_to_name_map,
        resource_groups
    )

    recipe_item = RecipeItem(
        name=id_to_name_map[input_struct.result.item_id],
        output=input_struct.result.count,
        recipe_type="Cutting",
        requirements={
            ingredient: 1
        }
    )
    return [recipe_item]

################################################################################
############################### Smithing Recipes ###############################
################################################################################
@dataclass
class SmithingData:
    recipe_type: Literal["minecraft:smithing_transform"] = field(metadata={"json": "type"})
    addition: ItemDict
    base: ItemDict
    result: Result
    template: ItemDict


def parse_smithing_transform_data(
    input_data: Any,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> List[RecipeItem]:
    input_struct = classnotation.load_data(SmithingData, input_data)

    addition: str = get_item_name_from_item_dict(input_struct.addition, id_to_name_map, resource_groups)
    base: str = get_item_name_from_item_dict(input_struct.base, id_to_name_map, resource_groups)

    return [
        RecipeItem(
            name=id_to_name_map[input_struct.result.item_id],
            output=input_struct.result.count,
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
def get_item_name_from_item_dict(
    itemdict: ItemDict,
    id_to_name_map: Dict[str, str],
    resource_groups: ResourceGroups,
) -> str:
    if isinstance(itemdict, ItemDictItem):
        return id_to_name_map[itemdict.item] 
    elif isinstance(itemdict, ItemDictTag):
        return resource_groups.get_display_name_from_group(itemdict.tag)
    elif isinstance(itemdict, list):
        return resource_groups.get_display_name_from_group(get_tag_from_itemdict_list(itemdict, resource_groups).tag)


def get_tag_from_itemdict_list(
    ingredient_list: List[ItemDictItem],
    resource_groups: ResourceGroups
) -> ItemDictTag:
    compact_list = sorted([x.item for x in ingredient_list])
    group_name = resource_groups.get_group_from_resources(compact_list)
    return ItemDictTag(tag=group_name)
