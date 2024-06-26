from recipe_item import RecipeItem
from typing import List

################################################################################
# recipes
#
# Custom bucket filling recipes. These are technically incompelte because they
# require an external block or entity, which we don't currently track in
# resource calculator. However, they do consume a bucket which should be
# tracked. So these add the bucket as a requirement and allow a location
# to track the blocks or entites later.
################################################################################
def recipes() -> List[RecipeItem]:
    buckets = { 
        "Water Bucket": "water block",
        "Lava Bucket": "lava block",
        "Powder Snow Bucket": "powder snow block",
        "Milk Bucket": "cow (infinite)",
        "Bucket of Pufferfish": "pufferfish in water",
        "Bucket of Salmon": "salmon in water",
        "Bucket of Cod": "cod in water",
        "Bucket of Tropical Fish": "tropical fish in water",
        "Bucket of Axolotl": "axolotl in water",
    }

    return [RecipeItem(
        name=x,
        output=1,
        recipe_type="Fill Bucket",
        requirements={
            "Bucket": 1
        }
    ) for x in buckets]
