from recipe_item import RecipeItem
from typing import List

oxidation_levels = [
    "",
    "Exposed ",
    "Weathered ",
    "Oxidized ",
]

replacements = {
    "Copper": "Block of Copper",
}

items = [
    "Copper",
    "Cut Copper",
    "Cut Copper Stairs",
    "Cut Copper Slab",
]

def maybe_replace_name(string):
    if string in replacements:
        return replacements[string]
    return string

def recipes():

    recipes: List[RecipeItem] = []

    for item in items:
        for oxidization_level in range(len(oxidation_levels)):
            oxidization = oxidation_levels[oxidization_level]

            for i in range(oxidization_level):
                required_oxidization = oxidation_levels[i]
                
                recipes.append(RecipeItem(
                    name=maybe_replace_name(oxidization+item),
                    output=1,
                    recipe_type="Oxidation",
                    requirements={
                        maybe_replace_name(required_oxidization+item): 1
                    }
                ))
    return recipes
