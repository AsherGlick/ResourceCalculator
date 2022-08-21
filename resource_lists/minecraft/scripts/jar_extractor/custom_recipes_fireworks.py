from recipe_item import RecipeItem
from typing import List

def recipes() -> List[RecipeItem]:
    return [
        RecipeItem(
            name="Firework Rocket",
            output=3,
            recipe_type="Crafting",
            requirements={
                "Paper": 1,
                "Gunpowder": 3
            }
        ),
        RecipeItem(
            name="Firework Rocket",
            output=3,
            recipe_type="Crafting",
            requirements={
                "Paper": 1,
                "Gunpowder": 2
            }
        ),
        RecipeItem(
            name="Firework Rocket",
            output=3,
            recipe_type="Crafting",
            requirements={
                "Paper": 1,
                "Gunpowder": 1
            }
        ),
    ]
