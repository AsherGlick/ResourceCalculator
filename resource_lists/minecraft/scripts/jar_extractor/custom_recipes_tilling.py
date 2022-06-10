from recipe_item import RecipeItem
from typing import List

def recipes() -> List[RecipeItem]:
    tillable_blocks = [
        "Dirt",
        "Grass Block",
        "Dirt Path"
    ]

    return [RecipeItem(
        name="Farmland",
        output=1,
        recipe_type="Till",
        requirements={
            x: 1
        } 
    ) for x in tillable_blocks]
