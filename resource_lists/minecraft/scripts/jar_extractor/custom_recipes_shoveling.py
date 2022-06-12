from recipe_item import RecipeItem
from typing import List

def recipes() -> List[RecipeItem]:
    shovelable_blocks = [
        "Dirt",
        "Grass Block",
        "Coarse Dirt",
        "Mycelium",
        "Podzol",
        "Rooted Dirt",
    ]

    return [RecipeItem(
        name="Dirt Path",
        output=1,
        recipe_type="Shovel",
        requirements={
            x: 1
        } 
    ) for x in shovelable_blocks]


