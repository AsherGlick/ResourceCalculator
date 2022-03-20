# This is designed as a reverse recipe lookup validator for the main recipe list
# for anything to do with the stonecutter. This is because it is easy to put a
# block in the stonecutter in-game and see all the things it can be cut into
# so it is easy to build a complete list of things that can be cut out of other
# blocks. This will then take that list and make sure those other blocks do 
# have recipes that include each of these source blocks.

# TODO: This is no longer 100% accurate because of how output quantity is
# assumed to be 1 unless they are slabs which are 2. As of 1.18 this is broken
# for copper blocks and the waxed / weathered variants when converting them
# into cut copper slabs. In this craft 8 are produced instead.

import yaml
from typing import Dict, List

stonecutter_results: Dict[str, List[str]] = {
	"Andesite": [
		"Andesite Slab",
		"Andesite Stairs",
		"Andesite Wall",
		"Polished Andesite",
		"Polished Andesite Slab",
	],
	"Basalt": [
		"Polished Basalt",
	],
	"Blackstone": [
		"Blackstone Slab",
		"Blackstone Stairs",
		"Blackstone Wall",
		"Chiseled Polished Blackstone",
		"Polished Blackstone",
		"Polished Blackstone Brick Slab",
		"Polished Blackstone Brick Stairs",
		"Polished Blackstone Brick Wall",
		"Polished Blackstone Bricks",
		"Polished Blackstone Slab",
		"Polished Blackstone Stairs",
		"Polished Blackstone Wall",
	],
	"Block of Copper": [
		"Cut Copper",
		"Cut Copper Slab",
		"Cut Copper Stairs",
	],
	"Block of Quartz": [
		"Chiseled Quartz Block",
		"Quartz Bricks",
		"Quartz Pillar",
		"Quartz Slab",
		"Quartz Stairs",
	],
	"Bricks": [
		"Brick Slab",
		"Brick Stairs",
		"Brick Wall",
	],
	"Cobblestone": [
		"Cobblestone Slab",
		"Cobblestone Stairs",
		"Cobblestone Wall",
	],
	"Cut Red Sandstone": [
		"Cut Red Sandstone Slab",
	],
	"Cut Sandstone": [
		"Cut Sandstone Slab",
	],
	"Dark Prismarine": [
		"Dark Prismarine Slab",
		"Dark Prismarine Stairs",
	],
	"Diorite": [
		"Diorite Slab",
		"Diorite Stairs",
		"Diorite Wall",
		"Polished Diorite",
		"Polished Diorite Slab",
		"Polished Diorite Stairs",
	],
	"End Stone": [
		"End Stone Brick Slab",
		"End Stone Brick Stairs",
		"End Stone Brick Wall",
		"End Stone Bricks",
	],
	"End Stone Bricks": [
		"End Stone Brick Slab",
		"End Stone Brick Stairs",
		"End Stone Brick Wall",
	],
	"Exposed Copper": [
		"Exposed Cut Copper",
		"Exposed Cut Copper Slab",
		"Exposed Cut Copper Stairs",
	],
	"Granite": [
		"Granite Slab",
		"Granite Stairs",
		"Granite Wall",
		"Polished Granite",
		"Polished Granite Slab",
		"Polished Granite Stairs",
	],
	"Mossy Cobblestone": [
		"Mossy Cobblestone Slab",
		"Mossy Cobblestone Stairs",
		"Mossy Cobblestone Wall",
	],
	"Mossy Stone Bricks": [
		"Mossy Stone Brick Slab",
		"Mossy Stone Brick Stairs",
		"Mossy Stone Brick Wall",
	],
	"Nether Bricks": [
		"Chiseled Nether Bricks",
		"Nether Brick Slab",
		"Nether Brick Stairs",
		"Nether Brick Wall",
	],
	"Oxidized Copper": [
		"Oxidized Cut Copper",
		"Oxidized Cut Copper Slab",
		"Oxidized Cut Copper Stairs",
	],
	"Polished Andesite": [
		"Polished Andesite Slab",
		"Polished Andesite Stairs",
	],
	"Polished Blackstone": [
		"Chiseled Polished Blackstone",
		"Polished Blackstone Brick Slab",
		"Polished Blackstone Brick Stairs",
		"Polished Blackstone Brick Wall",
		"Polished Blackstone Bricks",
		"Polished Blackstone Slab",
		"Polished Blackstone Stairs",
		"Polished Blackstone Wall",
	],
	"Polished Diorite": [
		"Polished Diorite Slab",
		"Polished Diorite Stairs",
	],
	"Polished Granite": [
		"Polished Granite Slab",
		"Polished Granite Stairs",
	],
	"Prismarine": [
		"Prismarine Slab",
		"Prismarine Stairs",
		"Prismarine Wall",
	],
	"Prismarine Bricks": [
		"Prismarine Brick Slab",
		"Prismarine Brick Stairs",
	],
	"Purpur Block": [
		"Purpur Pillar",
		"Purpur Slab",
		"Purpur Stairs",
	],
	"Red Nether Bricks": [
		"Red Nether Brick Slab",
		"Red Nether Brick Stairs",
		"Red Nether Brick Wall",
	],
	"Red Sandstone": [
		"Chiseled Red Sandstone",
		"Cut Red Sandstone",
		"Cut Red Sandstone Slab",
		"Red Sandstone Slab",
		"Red Sandstone Stairs",
		"Red Sandstone Wall",
	],
	"Sandstone": [
		"Chiseled Sandstone",
		"Cut Sandstone",
		"Cut Sandstone Slab",
		"Sandstone Slab",
		"Sandstone Stairs",
		"Sandstone Wall",
	],
	"Smooth Quartz Block": [
		"Smooth Quartz Slab",
		"Smooth Quartz Stairs",
	],
	"Smooth Red Sandstone": [
		"Smooth Red Sandstone Slab",
		"Smooth Red Sandstone Stairs",
	],
	"Smooth Sandstone": [
		"Smooth Sandstone Slab",
		"Smooth Sandstone Stairs",
	],
	"Smooth Stone": [
		"Smooth Stone Slab"
	],
	"Stone": [
		"Chiseled Stone Bricks",
		"Stone Brick Slab",
		"Stone Brick Stairs",
		"Stone Brick Wall",
		"Stone Bricks",
		"Stone Slab",
		"Stone Stairs",
	],
	"Stone Bricks": [
		"Chiseled Stone Bricks",
		"Stone Brick Slab",
		"Stone Brick Stairs",
		"Stone Brick Wall",
	],
	"Waxed Block of Copper": [
		"Waxed Cut Copper",
		"Waxed Cut Copper Slab",
		"Waxed Cut Copper Stairs",
	],
	"Waxed Exposed Copper": [
		"Waxed Exposed Cut Copper",
		"Waxed Exposed Cut Copper Slab",
		"Waxed Exposed Cut Copper Stairs",
	],
	"Waxed Oxidized Copper": [
		"Waxed Oxidized Cut Copper",
		"Waxed Oxidized Cut Copper Slab",
		"Waxed Oxidized Cut Copper Stairs",
	],
	"Waxed Weathered Copper": [
		"Waxed Weathered Cut Copper",
		"Waxed Weathered Cut Copper Slab",
		"Waxed Weathered Cut Copper Stairs",
	],
	"Weathered Copper": [
		"Weathered Cut Copper",
		"Weathered Cut Copper Slab",
		"Weathered Cut Copper Stairs",
	],
}


inverted_stonecutter_results = {}

for source_block in stonecutter_results:
	for result_block in stonecutter_results[source_block]:
		if result_block not in inverted_stonecutter_results:
			inverted_stonecutter_results[result_block] = []
		inverted_stonecutter_results[result_block].append(source_block)


with open("../resources.yaml") as f:
	resources = yaml.safe_load(f.read())["resources"]


for resource in inverted_stonecutter_results:
	# TODO: This is no longer 100% accurate, see note at top of file.
	quantity = 1
	if resource.endswith("Slab"):
		quantity = 2
	if resource not in resources:
		print("{} not found in resources.yaml".format(resource))

	recipes = resources[resource]["recipes"]

	for crafted_from in inverted_stonecutter_results[resource]:
		target_recipe = {'output': quantity, 'recipe_type': 'Cutting', 'requirements': {crafted_from: -1}}

		found = False
		for recipe in recipes:
			if target_recipe == recipe:
				found = True

		if not found:
			print("Could not find cutting recipe to create \"{}\" from \"{}\"".format(resource, crafted_from))
			print("ADD RECIPE:")
			print("    - output: {}".format(str(quantity)))
			print("      recipe_type: Cutting")
			print("      requirements:")
			print("        {}: -1".format(crafted_from))
			print("")
