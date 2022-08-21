from recipe_item import RecipeItem
from typing import List
from colors import colors


def recipes() -> List[RecipeItem]:
    return [RecipeItem(
        name="Obsidian",
        output=1,
        recipe_type="Add Water",
        requirements={
            "Lava Bucket": 1
        } 
    )] + concrete_recipes()


def concrete_recipes() -> List[RecipeItem]:
    return [RecipeItem(
        name=color + " Concrete",
        output=1,
        recipe_type="Add Water",
        requirements={
            color + " Concrete Powder": 1
        } 
    ) for color in colors()]
