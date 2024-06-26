from recipe_item import RecipeItem
from typing import List, Dict
from requirement_groups import ResourceGroups
import re

# Take the input of the jar tags for "logs" and if there is a stripped version
# of any log then add a recipe of converting that log to the stripped version.
def recipes(resource_groups: ResourceGroups, id_to_name: Dict[str, str]) -> List[RecipeItem]:
    recipes: List[RecipeItem] = []


    # Logs
    log_types: List[str] = resource_groups.get_resouces_from_group("minecraft:logs")
    recipes += build_stripped_recipes(log_types, id_to_name)

    # Bamboo
    bamboo_types: List[str] = resource_groups.get_resouces_from_group("minecraft:bamboo_blocks")
    recipes += build_stripped_recipes(bamboo_types, id_to_name)

    return recipes

def build_stripped_recipes(item_category_ids: List[str], id_to_name: Dict[str, str]) -> List[RecipeItem]:
    recipes: List[RecipeItem] = []
    for item_id in item_category_ids:
        stripped_item_id = get_stripped_variant_id(item_id)

        if stripped_item_id not in item_category_ids:
            continue

        recipes.append(RecipeItem(
            name=id_to_name[stripped_item_id],
            output=1,
            recipe_type="Strip",
            requirements={
                id_to_name[item_id]: 1
            }
        ))

    return recipes


################################################################################
# get_stripped_variaint_id
#
# Adds a "stripped_" prefix to the name of the item after the namespace.
# `minecraft:oak_log` becomes `minecraft:stripped_oak_log`
################################################################################
def get_stripped_variant_id(log_id: str) -> str:
    match = re.match(r"([^:]*):(.*)", log_id)

    if match is None:
        raise ValueError("Invalid minecraft id {}".format(log_id))

    prefix = match.group(1)
    suffix = match.group(2)

    return f"{prefix}:stripped_{suffix}"
