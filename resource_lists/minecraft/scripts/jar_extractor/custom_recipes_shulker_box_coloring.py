from recipe_item import RecipeItem
from typing import List
from colors import colors


def recipes() -> List[RecipeItem]:
    return [RecipeItem(
        name=color+" Shulker Box",
        output=1,
        recipe_type="Crafting",
        requirements={
            "Any Shulker Box": 1,
            color + " Dye": 1
        } 
    ) for color in colors()]
