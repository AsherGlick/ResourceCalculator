from dataclasses import dataclass
from typing import Dict

@dataclass
class RecipeItem():
    name: str
    output: int
    recipe_type: str
    requirements: Dict[str, int]

