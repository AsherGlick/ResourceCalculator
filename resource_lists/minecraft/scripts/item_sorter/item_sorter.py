import sys

# Include the standard resource list parsing library
sys.path.append("../../../../")
from pylib.yaml_token_load import ordered_load
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, TokenError, Token, get_primitive, Heading

from typing import Iterable, List, OrderedDict, Dict, Union, Tuple
from functools import cmp_to_key

import json


def main():
    errors: List[TokenError] = []
    with open("../../resources.yaml", 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    resource_list.resources = sorted_resources(resource_list.resources)

    with open("./resources.yaml", "w", encoding="utf_8") as f:
        f.write(
            resource_list.to_yaml()
        )

def get_compressed_name_map(names: Iterable[str]) -> Dict[str, str]:
    output_map: Dict[str, str] = {}
    for name in names:
        compressed_name = name.replace(" ", "")
        output_map[compressed_name] = name
    return output_map

def custom_items() -> List[str]:
    return [
        "Fuel",
    ]

def is_expected_missing_item(item: str) -> bool:
    if item.endswith("SpawnEgg"):
        return True

    if item.endswith("PotterySherd"):
        return True

    if item.startswith("LingeringPotionof"):
        return True

    if item.startswith("SplashPotionof"):
        return True

    if item.startswith("Potionof"):
        return True

    if item.startswith("Arrowof"):
        return True

    if item in (
        "AwkwardLingeringPotion",
        "AwkwardPotion",
        "AwkwardSplashPotion",
        "ChippedAnvil",
        "DamagedAnvil",
        "DragonEgg",
        "EnchantedBook",
        "LingeringWaterBottle",
        "MonsterSpawner",
        "MundaneLingeringPotion",
        "MundanePotion",
        "MundaneSplashPotion",
        "OminousBottle",
        "OminousTrialKey",
        "SmithingTemplate",
        "SplashWaterBottle",
        "SuspiciousStew",
        "ThickLingeringPotion",
        "ThickPotion",
        "ThickSplashPotion",
        "TippedArrow",
        "TrialKey",
        "TrialSpawner",
        "TropicalFish",
        "Vault",
    ):
        return True

    return False

visited_items = set()
def sorted_resources(resources: List[Union[Resource, Heading]]) -> List[Union[Resource, Heading]]:
    with open("./item_ordering.json") as f:
        item_order = json.load(f)
    item_order += custom_items()

    resource_map = {x.name: x for x in resources if not isinstance(x, Heading)}
    expanded_names = get_compressed_name_map([k for k in resource_map.keys()])

    new_ordered_resources: List[Union[Resource, Heading]] = []

    for item in item_order:
        if item in visited_items:
            continue
        visited_items.add(item)

        expanded_name = expanded_names.get(item, None)
        if expanded_name is None:
            if is_expected_missing_item(item):
                continue
            print("Missing: ", item)
            continue
        
        new_ordered_resources.append(resource_map[expanded_name])
        del resource_map[expanded_name] # This will probalby cause errors because of duplicates

    if len(resource_map) > 0:
        print("Some Resources Are Remaining", resource_map.keys())
    return new_ordered_resources

if __name__ == "__main__":
    main()
