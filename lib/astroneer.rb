module Astroneer
	@astroneer_recipes = {
		"Coal" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Coal" => 0}
			},
		],
		"Compound" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Compound" => 0}
			},
		],
		"Laterite" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Laterite" => 0}
			},
		],
		"Malachite" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Malachite" => 0}
			},
		],
		"Hydrazine" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Hydrazine" => 0}
			},
		],
		"Lithium" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Lithium" => 0}
			},
		],
		"Organic" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Organic" => 0}
			},
		],
		"Oxygen" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Oxygen" => 0}
			},
		],
		"Power" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Power" => 0}
			},
		],
		"Resin" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Resin" => 0}
			},
		],
		"Titanium" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Titanium" => 0}
			},
		],
		"Aluminum" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Aluminum" => 0}
			},
			{
				output: 1,
				recipe_type: "Smelter",
				requirements: {"Laterite" => -1}
			}
		],
		"Copper" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
				requirements: {"Copper" => 0}
			},
			{
				output: 1,
				recipe_type: "Smelter",
				requirements: {"Malachite" => -1}
			}
		],
		"Tethers" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Compound" => -1}
			}
		],
		"Small Solar Panel" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Compound" => -1}
			}
		],
		"Small Wind Turbine" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Aluminum" => -1}
			}
		],
		"Small Generator" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Copper" => -1}
			}
		],
		"Small Battery" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Lithium" => -1}
			}
		],
		"Power Cells" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Compound" => -1}
			}
		],
		"Tank" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Compound" => -1}
			}
		],
		"Filters" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Compound" => -1}
			}
		],
		"Narrow Mod" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Copper" => -1}
			}
		],
		"Wide Mod" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Copper" => -1}
			}
		],
		"Inhibitor Mod" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Copper" => -1}
			}
		],

		"Terrain Analyzer" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Aluminum" => -1}
			}
		],
		"Dynamite" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Aluminum" => -1}
			}
		],
		"Beacon" => [
			{
				output: 1,
				recipe_type: "Backpack Printer",
				requirements: {"Compound" => -1}
			}
		],
		"1-Seat" => [
			{
				output: 1,
				recipe_type: "Printer and Vehicle Bay",
				requirements: {"Compound" => -2}
			}
		],
		"Medium Storage" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Compound" => -2}
			}
		],
		"Medium Wind Turbine" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Aluminum" => -2}
			}
		],
		"Drill Head" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Aluminum" => -2}
			}
		],
		"Medium Battery" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Lithium" => -2}
			}
		],
		"Medium Generator" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Copper" => -2}
			}
		],
		"Habitat" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Compound" => -2}
			}
		],
		"Solar Panel" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Compound" => -2}
			}
		],
		"Winch" => [
			{
				output: 1,
				recipe_type: "Printer",
				requirements: {"Titanium" => -2}
			}
		],
		"Thruster" => [
			{
				output: 1,
				recipe_type: "Raw Resource",
			}
		],
		"Research Station" => [
			{
				output: 1,
				recipe_type: "Large Platform",
				requirements: {"Compound" => -2}
			}
		],
		"Fuel Condenser" => [
			{
				output: 1,
				recipe_type: "Large Platform",
				requirements: {"Copper" => -2}
			}
		],
		"Medium Printer" => [
			{
				output: 1,
				recipe_type: "Large Platform",
				requirements: {"Copper" => -2}
			}
		],
		"Smelter" => [
			{
				output: 1,
				recipe_type: "Large Platform",
				requirements: {"Compound" => -2}
			}
		],
		"Vehicle Bay" => [
			{
				output: 1,
				recipe_type: "Large Platform",
				requirements: {"Aluminum" => -2}
			}
		],
		"Trade Platform" => [
			{
				output: 1,
				recipe_type: "Large Platform",
				requirements: {"Aluminum" => -2}
			}
		],
		"3-Seat" => [
			{
				output: 1,
				recipe_type: "Vehicle Bay",
				requirements: {"Copper" => -4}
			}
		],
		"Large Storage" => [
			{
				output: 1,
				recipe_type: "Vehicle Bay",
				requirements: {"Compound" => -4}
			}
		],
		"Crane" => [
			{
				output: 1,
				recipe_type: "Vehicle Bay",
				requirements: {"Copper" => -4}
			}
		],
		"Medium Rover" => [
			{
				output: 1,
				recipe_type: "Vehicle Bay",
				requirements: {"Compound" => -2}
			}
		],
		"Large Rover" => [
			{
				output: 1,
				recipe_type: "Vehicle Bay",
				requirements: {"Aluminum" => -4}
			}
		],
		"Shuttle" => [
			{
				output: 1,
				recipe_type: "Vehicle Bay",
				requirements: {"Compound" => -2}
			}
		],
		"Large Shuttle" => [
			{
				output: 1,
				recipe_type: "Vehicle Bay",
				requirements: {"Copper" => -4}
			}
		],
		# "Copper"	
		# "Astronium"	N/A	N/A
		# "Hematite"	N/A	N/A
		# "Artifacts"	N/A	N/A
		# "Marbles"	N/A	N/A
		# "Terrain Tool"	N/A	N/A
		# "Solar Array" (Wrecks)	N/A	N/A
	}







		

	def self.item_list
		return @astroneer_recipes
		# output_list = {}
		# for item in @minecraft_recipes
		# 	name = item[:name]
		# 	recipes = item[:recipes]

		# 	for recipe in recipes


		# 		required_resources = Hash.new(0)

		# 		if (recipe[:recipe_type] == "Raw Resource")
		# 			# Create a dummy value that will show up for recipe selection
		# 			# but will not effect the overall crafting calculation
		# 			required_resources[name] = 0
		# 		else
		# 			# iterate over the array, counting duplicate entries
		# 			recipe[:recipe].each do |recipe_item|
		# 				if (recipe_item != nil)
		# 					required_resources[recipe_item] -= 1
		# 				end
		# 			end
		# 		end
		# 		recipe[:requirements] = required_resources
		# 	end


		# 	output_list[name] = recipes
		# end
		# return output_list
	end
end
