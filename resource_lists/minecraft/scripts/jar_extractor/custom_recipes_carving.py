from recipe_item import RecipeItem
from typing import List

def recipes() -> List[RecipeItem]:
    return [RecipeItem(
        name="Carved Pumpkin",
        output=1,
        recipe_type="Carve",
        requirements={
            "Pumpkin": 1
        }
    )]