# require 'recipes'
class StructureController < ApplicationController

  def index
  	@name_mappings = Recipes.minecraft_name_map
  	@properties = Recipes.property_map
  	@recipie_count = Recipes.recipe_count

  	# # not variant
  	# # these are properties that are only present in the block and not the item
  	# @block_only_properties = [
  	# 	'facing',
  	# 	'rotation',
  	# 	'occupied',#bed
  	# 	'part', #bed
  	# 	'age', #plant
  	# 	'axis', #boneblock
  	# 	'has_bottle_0',
  	# 	'has_bottle_1',
  	# 	'has_bottle_2',
  	# 	'powered',
  	# 	'bites',
  	# 	'level', #cauldron
  	# 	'north', #chorus plant
  	# 	'south', #chorus plant
  	# 	'east', #chorus plant
  	# 	'west', #chorus plant
  	# 	'up', #chrous plant
  	# 	'down' # chrous plant
  	# 	'power'
  	# 	'snowy'
  	# 	'triggered', # dispenser
  	# 	'half', # wooden door
  	# 	'hinge', # wooden door
  	# 	'open', # wooden door
  	# 	'powered', #wooden door
  	# 	'eye', #end portal frame
  	# 	'moisture', #farmland
  	# 	'in_wapp', #fencegate
  	# 	'contents', #flower pot
  	# 	'legacy_data', #flower_pot (hopefully this is not overused)
  	# 	'enabled', #hopper
  	# 	'has_record', #jukebox
  	# 	'check_decay', #leaves
  	# 	'decayable', #leaves
  	# 	'extended', #pistons
  	# 	'shape', #rails
  	# 	'mode', # comparitor
  	# 	'delay', # repeater
  	# 	'stage', #sapling
  	# 	'nodrop', #skull
  	# 	'attached', #tripwire
  	# 	'disarmed', #tripwire


  	# ]


  end
end



# ##############
# anvil: damage
# carpet: color
# cobblestone_wall: variant
# flowers: type
# sponge: wet

# snow_layer: layers # this will be unique to snow because of how multiple layers means multipe items







# ##################
# dobule stone slabs have the "seemless" property but I dont htink they are even items and that property can only be set via commands
# tnt has the "explode" property that I think can also only be set via command and does not exist in item form


# # note: mushroom blocks have many varients but possibly only one item




# ###########
# ignore_list