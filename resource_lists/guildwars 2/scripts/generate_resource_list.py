import urllib.request
import json
import sys
import os
from typing import List
import yaml

def get(url):
	return json.loads(urllib.request.urlopen(url).read())


item_list = []
def get_item_list() -> List[str]:
	global item_list
	if len(item_list) > 0:
		return item_list
	# urllib.request.urlopen("http://example.com/foo/bar").read()
	raw_item_list = get("https://api.guildwars2.com/v2/items")
	for item in raw_item_list:
		item_list.append(str(item))
	return item_list

recipe_list = []
def get_recipe_list():
	global recipe_list
	if len(recipe_list) > 0:
		return recipe_list

	raw_recipe_list = get("https://api.guildwars2.com/v2/recipes")
	for recipe in raw_recipe_list:
		recipe_list.append(str(recipe))
	return recipe_list


################################################################################
# Items Cache
################################################################################
item_cache_file = "items_cache.json"
item_cache_updated = 0
items_cache = {}
if os.path.isfile(item_cache_file):
	print("LOADING ITEMS CACHE")
	with open(item_cache_file, 'r') as f:
		items_cache = json.load(f)
# Maybe this can be used for faster retreaval!?!!!!!!!!!!!!
# https://api.guildwars2.com/v2/items?ids=12244&lang=en
def get_item(item_id):
	global items_cache
	global item_cache_updated

	if str(item_id) not in items_cache:
		print("ITEMS CACHE MISS", item_id)
		item_data = get("https://api.guildwars2.com/v2/items/" + str(item_id))
		items_cache[str(item_id)] = item_data
		item_cache_updated += 1
	return items_cache[str(item_id)]
def save_item_cache(force_cache=False):
	global item_cache_updated

	if item_cache_updated > 100 or (force_cache and item_cache_updated > 0):
		with open(item_cache_file, 'w') as f:
			json.dump(items_cache, f)
		print("Item Cache Updated")
		item_cache_updated = 0
def prune_items_cache():
	global items_cache
	global item_cache_updated
	items_to_delete = []
	item_set = set(item_list)
	for item in items_cache.keys():
		if type(item) != str:
			print("non string item key")
		if str(item) not in item_set:
			items_to_delete.append(item)

	for item in items_to_delete:
		item_cache_updated += 1
		del items_cache[item]

	print("items to delete", item_cache_updated)

	save_item_cache(True)



################################################################################
#
################################################################################
recipe_cache_file = "recipe_cache.json"
recipe_cache_updated = 0
recipe_cache = {}
if os.path.isfile(recipe_cache_file):
	print("LOADING RECIPE CACHE")
	with open(recipe_cache_file, 'r') as f:
		recipe_cache = json.load(f)
def get_recipe(recipe_id):
	global recipe_cache
	global recipe_cache_updated

	if str(recipe_id) not in recipe_cache:
		print("RECIPE CACHE MISS", recipe_id)
		recipe_data = get("https://api.guildwars2.com/v2/recipes/" + str(recipe_id))
		recipe_cache[str(recipe_id)] = recipe_data
		recipe_cache_updated += 1
	return recipe_cache[str(recipe_id)]
def save_recipe_cache(force_cache=False):
	global recipe_cache_updated

	if recipe_cache_updated > 100 or (force_cache and recipe_cache_updated > 0):
		with open(recipe_cache_file, 'w') as f:
			json.dump(recipe_cache, f)
		print("Recipe Cache Updated")
		recipe_cache_updated = 0
def prune_recipe_cache():
	global recipe_cache
	global recipe_cache_updated
	recipes_to_delete = []
	recipe_set = set(recipe_list)
	for recipe in recipe_cache.keys():
		if type(recipe) != str:
			print("non string recipe key")
		if str(recipe) not in recipe_set:
			recipes_to_delete.append(recipe)

	for recipe in recipes_to_delete:
		recipe_cache_updated += 1
		del recipe_cache[recipe]

	print("recipes to delete", recipe_cache_updated)

	save_item_cache(True)



import re
def simple_name(name: str) -> str:
    return re.sub(r'[^a-z0-9]', '', name.lower())

# def download_file(url):
#     local_filename = url.split('/')[-1]
#     # NOTE the stream=True parameter below
#     with urllib.requests.get(url, stream=True) as r:
#         r.raise_for_status()
#         with open(local_filename, 'wb') as f:
#             for chunk in r.iter_content(chunk_size=8192): 
#                 # If you have chunk encoded response uncomment if
#                 # and set chunk_size parameter to None.
#                 #if chunk: 
#                 f.write(chunk)
#     return local_filename

def main():
	used_or_consumed_items = set()

	item_list = get_item_list()
	for item in item_list:
		if type(item) != str:
			print("NON STR ITEM LIST")
			exit()
	print(len(item_list))
	recipe_list = get_recipe_list()
	print(len(recipe_list))	

	for (i, item) in enumerate(item_list):
		get_item(item)
		sys.stdout.write(str(i) + "/" + str(len(item_list)) + "\r")
		save_item_cache()

	save_item_cache(True)
	prune_items_cache()

	print("")

	for (i, recipe) in enumerate(recipe_list):
		recipe = get_recipe(recipe)
		sys.stdout.write(str(i) + "/" + str(len(recipe_list)) + "\r")
		save_recipe_cache()

	save_recipe_cache(True)
	prune_recipe_cache()
	print("")




	# identify bad recipes
	valid_recipe_list = []
	item_set = set(item_list)
	for (i, recipe_id) in enumerate(recipe_list):
		recipe = get_recipe(recipe_id)
		
		if str(recipe["output_item_id"]) not in item_set:

			print("bad recipe output", recipe_id, recipe["output_item_id"])
			continue
		for item in recipe["ingredients"]:
			if str(item["item_id"]) not in item_set:
				print("bad recipe input", recipe_id, item["item_id"])
				continue

		valid_recipe_list.append(recipe_id)


	associated_recipes = {}

	for recipe_id in valid_recipe_list:
		recipe = get_recipe(recipe_id)

		used_or_consumed_items.add(recipe["output_item_id"])
		for item in recipe["ingredients"]:
			used_or_consumed_items.add(item["item_id"])





		if recipe["output_item_id"] not in associated_recipes:
			associated_recipes[recipe["output_item_id"]] = []

		associated_recipes[recipe["output_item_id"]].append(recipe_id)




	print(len(used_or_consumed_items))





	for item_id in used_or_consumed_items:
		item = get_item(item_id)
		simplename = simple_name(item["name"])
		path = os.path.join("../items", simplename + ".png")

		if not os.path.exists(path):
			print(item["icon"], path)
			urllib.request.urlretrieve(item["icon"], path)



	output_yaml_resources = {}
	for item_id in used_or_consumed_items:
		item_name = get_item(item_id)["name"]

		recipes = []

		if item_id in associated_recipes:
			for recipe_id in associated_recipes[item_id]:
				recipe = get_recipe(recipe_id)
				requirements = {}
				for requirement in recipe["ingredients"]:
					requirements[get_item(requirement["item_id"])["name"]] = -requirement["count"]

				recipes.append(
					{
						"output": 1,
						"recipe_type":"Crafting",
						"requirements": requirements
					}
				)

		recipes.append({"recipe_type":"Raw Resource"})

		item_chunk = {"recipes": recipes} 

		output_yaml_resources[item_name] = item_chunk

	output_yaml_dump = {
		"authors": {"Asher": ""},
		"index_page_display_name": "Guild Wars 2",
		"recipe_types": {"Crafting": r"Craft {IN_ITEMS} into {OUT_ITEM}"},
		"resources": output_yaml_resources
	}


	with open("../resources.yaml", "w") as f:
		yaml.dump(output_yaml_dump, f)


if __name__ == "__main__":
	main()