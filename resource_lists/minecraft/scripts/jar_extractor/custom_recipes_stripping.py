from recipe_item import RecipeItem
from typing import List

# Take the input of the jar tags for "logs" and if there is a stripped version
# of any log then add a recipe of converting that log to the stripped version.
def recipes(logs_tag) -> List[RecipeItem]:
    recipes: List[RecipeItem] = []

    for wood in logs_tag:
        if "Stripped " + wood not in logs_tag:
            continue

        recipes.append(RecipeItem(
            name="Stripped " + wood,
            output=1,
            recipe_type="Strip",
            requirements={
                wood: 1
            }
        ))

    return recipes