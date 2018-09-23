module Minecraft
	@minecraft_recipes = {
		name: "Stone",
		minecraft_names: ["minecraft:stone:stone"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Cobblestone", "Fuel"],
			}
		],
	},{
		name: "Granite",
		minecraft_names: ["minecraft:stone:granite"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Diorite","Nether Quartz",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Polished Granite",
		minecraft_names: ["minecraft:stone:smooth_granite"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Granite","Granite",nil,"Granite","Granite",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diorite",
		minecraft_names: ["minecraft:stone:diorite"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Nether Quartz","Cobblestone",nil,"Cobblestone","Nether Quartz",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Polished Diorite",
		minecraft_names: ["minecraft:stone:smooth_diorite"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Diorite","Diorite",nil,"Diorite","Diorite",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Andesite",
		minecraft_names: ["minecraft:stone:andesite"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Diorite","Cobblestone",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Polished Andesite",
		minecraft_names: ["minecraft:stone:smooth_andesite"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Andesite","Andesite",nil,"Andesite","Andesite",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Grass Block",
		minecraft_names: ["minecraft:grass", "minecraft:grass_path"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dirt",
		minecraft_names: ["minecraft:dirt:dirt", "minecraft:farmland"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
		],
	},{
		name: "Coarse Dirt",
		minecraft_names: ["minecraft:dirt:coarse_dirt"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Gravel","Dirt",nil,"Dirt","Gravel",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Podzol",
		minecraft_names: ["minecraft:dirt:podzol"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cobblestone",
		minecraft_names: ["minecraft:cobblestone"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Wood Planks",
		minecraft_names: ["minecraft:planks:oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,nil,nil,nil,"Oak Wood",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Wood Planks",
		minecraft_names: ["minecraft:planks:spruce"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,nil,nil,nil,"Spruce Wood",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Wood Planks",
		minecraft_names: ["minecraft:planks:birch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,nil,nil,nil,"Birch Wood",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Wood Planks",
		minecraft_names: ["minecraft:planks:jungle"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,nil,nil,nil,"Jungle Wood",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Wood Planks",
		minecraft_names: ["minecraft:planks:acacia"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,nil,nil,nil,"Acacia Wood",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Wood Planks",
		minecraft_names: ["minecraft:planks:dark_oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,nil,nil,nil,"Dark Oak Wood",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bedrock",
		minecraft_names: ["minecraft:bedrock"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sand",
		minecraft_names: ["minecraft:sand:sand"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Sand",
		minecraft_names: ["minecraft:sand:red_sand"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gravel",
		minecraft_names: ["minecraft:gravel"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gold Ore",
		minecraft_names: ["minecraft:gold_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Ore",
		minecraft_names: ["minecraft:iron_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Coal Ore",
		minecraft_names: ["minecraft:coal_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Wood",
		minecraft_names: ["minecraft:log:oak"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Wood",
		minecraft_names: ["minecraft:log:spruce"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Wood",
		minecraft_names: ["minecraft:log:birch"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Wood",
		minecraft_names: ["minecraft:log:jungle"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sponge",
		minecraft_names: ["minecraft:sponge:false"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Wet Sponge", "Fuel"],
			}
		],
	},{
		name: "Wet Sponge",
		minecraft_names: ["minecraft:sponge:true"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Glass",
		minecraft_names: ["minecraft:glass"],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Sand", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Red Sand", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lapis Lazuli Ore",
		minecraft_names: ["minecraft:lapis_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lapis Lazuli Block",
		minecraft_names: ["minecraft:lapis_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Lapis Lazuli","Lapis Lazuli","Lapis Lazuli","Lapis Lazuli","Lapis Lazuli","Lapis Lazuli","Lapis Lazuli","Lapis Lazuli","Lapis Lazuli"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sandstone",
		minecraft_names: ["minecraft:sandstone:sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Sand","Sand",nil,"Sand","Sand",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chiseled Sandstone",
		minecraft_names: ["minecraft:sandstone:chiseled_sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Sandstone Slab",nil,nil,"Sandstone Slab",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Smooth Sandstone",
		minecraft_names: ["minecraft:sandstone:smooth_sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Sandstone","Sandstone",nil,"Sandstone","Sandstone",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wool",
		minecraft_names: ["minecraft:wool:white"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["String","String",nil,"String","String",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Wool",
		minecraft_names: ["minecraft:wool:orange"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Orange Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}

		],
	},{
		name: "Magenta Wool",
		minecraft_names: ["minecraft:wool:magenta"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Magenta Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Wool",
		minecraft_names: ["minecraft:wool:light_blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Light Blue Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Wool",
		minecraft_names: ["minecraft:wool:yellow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Dandelion Yellow",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Wool",
		minecraft_names: ["minecraft:wool:lime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Lime Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Wool",
		minecraft_names: ["minecraft:wool:pink"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Pink Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Wool",
		minecraft_names: ["minecraft:wool:gray"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Gray Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Wool",
		minecraft_names: ["minecraft:wool:silver"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Light Gray Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Wool",
		minecraft_names: ["minecraft:wool:cyan"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Cyan Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Wool",
		minecraft_names: ["minecraft:wool:purple"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Purple Dye",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Wool",
		minecraft_names: ["minecraft:wool:blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Lapis Lazuli",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Wool",
		minecraft_names: ["minecraft:wool:brown"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Cocoa Beans",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Wool",
		minecraft_names: ["minecraft:wool:green"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Cactus Green",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Wool",
		minecraft_names: ["minecraft:wool:red"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Rose Red",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Wool",
		minecraft_names: ["minecraft:wool:black"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wool","Ink Sac",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Gold",
		minecraft_names: ["minecraft:gold_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Iron",
		minecraft_names: ["minecraft:iron_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Slab",
		minecraft_names: ["minecraft:stone_slab:stone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Stone","Stone","Stone",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sandstone Slab",
		minecraft_names: ["minecraft:stone_slab:sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Sandstone","Sandstone","Sandstone",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cobblestone Slab",
		minecraft_names: ["minecraft:stone_slab:cobblestone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Cobblestone","Cobblestone","Cobblestone",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bricks Slab",
		minecraft_names: ["minecraft:stone_slab:brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Bricks","Bricks","Bricks",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Bricks Slab",
		minecraft_names: ["minecraft:stone_slab:stone_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Stone Brick","Stone Brick","Stone Brick",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Brick Slab",
		minecraft_names: ["minecraft:stone_slab:nether_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Nether Brick Block","Nether Brick Block","Nether Brick Block",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Quartz Slab",
		minecraft_names: ["minecraft:stone_slab:quartz"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Block of Quartz","Block of Quartz","Block of Quartz",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bricks",
		minecraft_names: ["minecraft:brick_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Brick","Brick",nil,"Brick","Brick",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bookshelf",
		minecraft_names: ["minecraft:bookshelf"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Book","Book","Book","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Moss Stone",
		minecraft_names: ["minecraft:mossy_cobblestone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone","Vines",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Obsidian",
		minecraft_names: ["minecraft:obsidian"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				output: 1,
				recipe_type: "add_water",
				recipe: ["Lava Bucket"]
			}
		],
	},{
		name: "Oak Wood Stairs",
		minecraft_names: ["minecraft:oak_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks",nil,"Oak Wood Planks","Oak Wood Planks",nil,nil,"Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Ore",
		minecraft_names: ["minecraft:diamond_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Diamond",
		minecraft_names: ["minecraft:diamond_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Diamond","Diamond","Diamond","Diamond","Diamond","Diamond","Diamond","Diamond","Diamond"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cobblestone Stairs",
		minecraft_names: ["minecraft:stone_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Cobblestone","Cobblestone","Cobblestone",nil,"Cobblestone","Cobblestone",nil,nil,"Cobblestone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Redstone Ore",
		minecraft_names: ["minecraft:lit_redstone_ore", "minecraft:redstone_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Ice",
		minecraft_names: ["minecraft:ice"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Snow",
		minecraft_names: ["minecraft:snow_layer"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Clay",
		minecraft_names: ["minecraft:clay"],
		recipes: [
			{
				output:1,
				recipe_type: "crafting",
				recipe: [nil,nil,nil,"Clay","Clay",nil,"Clay","Clay",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pumpkin",
		minecraft_names: ["minecraft:pumpkin"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Netherrack",
		minecraft_names: ["minecraft:netherrack"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Soul Sand",
		minecraft_names: ["minecraft:soul_sand"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Glowstone",
		minecraft_names: ["minecraft:glowstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Glowstone Dust","Glowstone Dust",nil,"Glowstone Dust","Glowstone Dust",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jack o'Lantern",
		minecraft_names: ["minecraft:lit_pumpkin"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Torch",nil,"Pumpkin",nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Stained Glass",
		minecraft_names: ["minecraft:stained_glass:white"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Bone Meal","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Stained Glass",
		minecraft_names: ["minecraft:stained_glass:orange"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Orange Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magenta Stained Glass",
		minecraft_names: ["minecraft:stained_glass:magenta"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Magenta Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Stained Glass",
		minecraft_names: ["minecraft:stained_glass:light_blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Light Blue Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Stained Glass",
		minecraft_names: ["minecraft:stained_glass:yellow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Dandelion Yellow","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Stained Glass",
		minecraft_names: ["minecraft:stained_glass:lime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Lime Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Stained Glass",
		minecraft_names: ["minecraft:stained_glass:pink"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Pink Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Stained Glass",
		minecraft_names: ["minecraft:stained_glass:gray"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Gray Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Stained Glass",
		minecraft_names: ["minecraft:stained_glass:silver"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Light Gray Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Stained Glass",
		minecraft_names: ["minecraft:stained_glass:cyan"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Cyan Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Stained Glass",
		minecraft_names: ["minecraft:stained_glass:purple"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Purple Dye","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Stained Glass",
		minecraft_names: ["minecraft:stained_glass:blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Lapis Lazuli","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Stained Glass",
		minecraft_names: ["minecraft:stained_glass:brown"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Cocoa Beans","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Stained Glass",
		minecraft_names: ["minecraft:stained_glass:green"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Cactus Green","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Stained Glass",
		minecraft_names: ["minecraft:stained_glass:red"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Rose Red","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Stained Glass",
		minecraft_names: ["minecraft:stained_glass:black"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Glass","Glass","Glass","Glass","Ink Sac","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Brick",
		minecraft_names: ["minecraft:stonebrick:stonebrick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Stone","Stone",nil,"Stone","Stone",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Mossy Stone Bricks",
		minecraft_names: ["minecraft:stonebrick:mossy_stonebrick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stone Brick","Vines",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cracked Stone Bricks",
		minecraft_names: ["minecraft:stonebrick:cracked_stonebrick"],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Stone Bricks", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chiseled Stone Bricks",
		minecraft_names: ["minecraft:stonebrick:chiseled_stonebrick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stone Bricks Slab",nil,nil,"Stone Bricks Slab",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Melon",
		minecraft_names: ["minecraft:melon_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Melon Slice","Melon Slice","Melon Slice","Melon Slice","Melon Slice","Melon Slice","Melon Slice","Melon Slice","Melon Slice"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brick Stairs",
		minecraft_names: ["minecraft:brick_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Bricks","Bricks","Bricks",nil,"Bricks","Bricks",nil,nil,"Bricks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Brick Stairs",
		minecraft_names: ["minecraft:stone_brick_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Stone Brick","Stone Brick","Stone Brick",nil,"Stone Brick","Stone Brick",nil,nil,"Stone Brick"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Mycelium",
		minecraft_names: ["minecraft:mycelium"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Brick Block",
		minecraft_names: ["minecraft:nether_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Nether Brick","Nether Brick",nil,"Nether Brick","Nether Brick",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Brick Stairs",
		minecraft_names: ["minecraft:nether_brick_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Nether Brick Block","Nether Brick Block","Nether Brick Block",nil,"Nether Brick Block","Nether Brick Block",nil,nil,"Nether Brick Block"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "End Stone",
		minecraft_names: ["minecraft:end_stone"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Wood Slab",
		minecraft_names: ["minecraft:wooden_slab:oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Wood Slab",
		minecraft_names: ["minecraft:wooden_slab:spruce"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Wood Slab",
		minecraft_names: ["minecraft:wooden_slab:birch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Birch Wood Planks","Birch Wood Planks","Birch Wood Planks",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Wood Slab",
		minecraft_names: ["minecraft:wooden_slab:jungle"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Wood Slab",
		minecraft_names: ["minecraft:wooden_slab:acacia"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Wood Slab",
		minecraft_names: ["minecraft:wooden_slab:dark_oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sandstone Stairs",
		minecraft_names: ["minecraft:sandstone_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Sandstone","Sandstone","Sandstone",nil,"Sandstone","Sandstone",nil,nil,"Sandstone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Emerald Ore",
		minecraft_names: ["minecraft:emerald_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Emerald",
		minecraft_names: ["minecraft:emerald_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Emerald","Emerald","Emerald","Emerald","Emerald","Emerald","Emerald","Emerald","Emerald"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Wood Stairs",
		minecraft_names: ["minecraft:spruce_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks",nil,"Spruce Wood Planks","Spruce Wood Planks",nil,nil,"Spruce Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Wood Stairs",
		minecraft_names: ["minecraft:birch_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Birch Wood Planks","Birch Wood Planks","Birch Wood Planks",nil,"Birch Wood Planks","Birch Wood Planks",nil,nil,"Birch Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Wood Stairs",
		minecraft_names: ["minecraft:jungle_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks",nil,"Jungle Wood Planks","Jungle Wood Planks",nil,nil,"Jungle Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cobblestone Wall",
		minecraft_names: ["minecraft:cobblestone_wall:cobblestone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Cobblestone","Cobblestone","Cobblestone","Cobblestone","Cobblestone","Cobblestone",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Mossy Cobblestone Wall",
		minecraft_names: ["minecraft:cobblestone_wall:mossy_cobblestone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Moss Stone","Moss Stone","Moss Stone","Moss Stone","Moss Stone","Moss Stone",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Quartz Ore",
		minecraft_names: ["minecraft:quartz_ore"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Quartz",
		minecraft_names: ["minecraft:quartz_block:default"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Nether Quartz","Nether Quartz",nil,"Nether Quartz","Nether Quartz",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chiseled Quartz Block",
		minecraft_names: ["minecraft:quartz_block:chiseled"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Quartz Slab",nil,nil,"Quartz Slab",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pillar Quartz Block",
		minecraft_names: ["minecraft:quartz_block:lines_z"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Block of Quartz",nil,nil,"Block of Quartz",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Quartz Stairs",
		minecraft_names: ["minecraft:quartz_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Block of Quartz","Block of Quartz","Block of Quartz",nil,"Block of Quartz","Block of Quartz",nil,nil,"Block of Quartz"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:white"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Bone Meal","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:orange"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Orange Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magenta Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:magenta"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Magenta Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:light_blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Light Blue Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:yellow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Dandelion Yellow","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:lime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Lime Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:pink"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Pink Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:gray"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Gray Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:silver"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Light Gray Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:cyan"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Cyan Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:purple"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Purple Dye","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Lapis Lazuli","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:brown"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Cocoa Beans","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:green"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Cactus Green","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:red"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Rose Red","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Terracotta",
		minecraft_names: ["minecraft:stained_hardened_clay:black"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Terracotta","Terracotta","Terracotta","Terracotta","Ink Sac","Terracotta","Terracotta","Terracotta","Terracotta"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Wood",
		minecraft_names: ["minecraft:log2:acacia"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Wood",
		minecraft_names: ["minecraft:log2:dark_oak"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Wood Stairs",
		minecraft_names: ["minecraft:acacia_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks",nil,"Acacia Wood Planks","Acacia Wood Planks",nil,nil,"Acacia Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Wood Stairs",
		minecraft_names: ["minecraft:dark_oak_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks",nil,"Dark Oak Wood Planks","Dark Oak Wood Planks",nil,nil,"Dark Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Prismarine",
		minecraft_names: ["minecraft:prismarine:prismarine"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Prismarine Shard","Prismarine Shard",nil,"Prismarine Shard","Prismarine Shard",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Prismarine Bricks",
		minecraft_names: ["minecraft:prismarine:prismarine_bricks"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Prismarine",
		minecraft_names: ["minecraft:prismarine:dark_prismarine"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard","Ink Sac","Prismarine Shard","Prismarine Shard","Prismarine Shard","Prismarine Shard"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sea Lantern",
		minecraft_names: ["minecraft:sea_lantern"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Prismarine Shard","Prismarine Crystals","Prismarine Shard","Prismarine Crystals","Prismarine Shard","Prismarine Crystals","Prismarine Shard","Prismarine Crystals","Prismarine Shard"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Hay Bale",
		minecraft_names: ["minecraft:hay_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wheat","Wheat","Wheat","Wheat","Wheat","Wheat","Wheat","Wheat","Wheat"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Terracotta",
		minecraft_names: ["minecraft:hardened_clay"],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Block of Clay", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Coal",
		minecraft_names: ["minecraft:coal_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Coal","Coal","Coal","Coal","Coal","Coal","Coal","Coal","Coal"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Packed Ice",
		minecraft_names: ["minecraft:packed_ice"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Sandstone",
		minecraft_names: ["minecraft:red_sandstone:red_sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Red Sand","Red Sand",nil,"Red Sand","Red Sand",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chiseled Red Sandstone",
		minecraft_names: ["minecraft:red_sandstone:chiseled_red_sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Red Sandstone Slab",nil,nil,"Red Sandstone Slab",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Smooth Red Sandstone",
		minecraft_names: ["minecraft:red_sandstone:smooth_red_sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Red Sandstone","Red Sandstone",nil,"Red Sandstone","Red Sandstone",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Sandstone Stairs",
		minecraft_names: ["minecraft:red_sandstone_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Red Sandstone","Red Sandstone","Red Sandstone",nil,"Red Sandstone","Red Sandstone",nil,nil,"Red Sandstone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Sandstone Slab",
		minecraft_names: ["minecraft:stone_slab2:red_sandstone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Red Sandstone","Red Sandstone","Red Sandstone",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purpur Block",
		minecraft_names: ["minecraft:purpur_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Popped Chorus Fruit","Popped Chorus Fruit",nil,"Popped Chorus Fruit","Popped Chorus Fruit",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purpur Pillar",
		minecraft_names: ["minecraft:purpur_pillar"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Purpur Slab",nil,nil,"Purpur Slab",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purpur Stairs",
		minecraft_names: ["minecraft:purpur_stairs"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Purpur Block","Purpur Block","Purpur Block",nil,"Purpur Block","Purpur Block",nil,nil,"Purpur Block"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purpur Slab",
		minecraft_names: ["minecraft:purpur_slab:default"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Purpur Block","Purpur Block","Purpur Block",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "End Stone Bricks",
		minecraft_names: ["minecraft:end_bricks"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["End Stone","End Stone",nil,"End Stone","End Stone",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magma Block",
		minecraft_names: ["minecraft:magma"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Magma Cream","Magma Cream",nil,"Magma Cream","Magma Cream",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Wart Block",
		minecraft_names: ["minecraft:nether_wart_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Nether Wart","Nether Wart","Nether Wart","Nether Wart","Nether Wart","Nether Wart","Nether Wart","Nether Wart","Nether Wart"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Nether Brick",
		minecraft_names: ["minecraft:red_nether_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Nether Brick","Nether Wart",nil,"Nether Wart","Nether Brick",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bone Block",
		minecraft_names: ["minecraft:bone_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Bone Meal","Bone Meal","Bone Meal","Bone Meal","Bone Meal","Bone Meal","Bone Meal","Bone Meal","Bone Meal"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Observer",
		minecraft_names: ["minecraft:observer"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Cobblestone","Cobblestone","Cobblestone","Redstone","Redstone","Nether Quartz","Cobblestone","Cobblestone","Cobblestone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Shulker Box",
		minecraft_names: ["minecraft:white_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Bone Meal", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Shulker Box",
		minecraft_names: ["minecraft:orange_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Orange Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magenta Shulker Box",
		minecraft_names: ["minecraft:magenta_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Magenta Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Shulker Box",
		minecraft_names: ["minecraft:light_blue_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Light Blue Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Shulker Box",
		minecraft_names: ["minecraft:yellow_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Dandelion Yellow", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Shulker Box",
		minecraft_names: ["minecraft:lime_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Lime Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Shulker Box",
		minecraft_names: ["minecraft:pink_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Pink Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Shulker Box",
		minecraft_names: ["minecraft:gray_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Gray Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Shulker Box",
		minecraft_names: ["minecraft:silver_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Light Gray Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Shulker Box",
		minecraft_names: ["minecraft:cyan_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Cyan Dye", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Shulker Box",
		minecraft_names: ["minecraft:purple_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:[nil,"Shulker Shell",nil, nil,"Chest",nil,nil,"Shulker Shell",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Shulker Box",
		minecraft_names: ["minecraft:blue_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Lapis Lazuli", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Shulker Box",
		minecraft_names: ["minecraft:brown_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Cocoa Beans", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Shulker Box",
		minecraft_names: ["minecraft:green_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Cactus Green", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Shulker Box",
		minecraft_names: ["minecraft:red_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Rose Red", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Shulker Box",
		minecraft_names: ["minecraft:black_shulker_box"],
		recipes: [
			{
				recipe_type: "crafting",
				output:1, 
				recipe:["Purple Shulker Box","Ink Sac", nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["White Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Orange Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Orange Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Magenta Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Magenta Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Light Blue Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Light Blue Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Yellow Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Yellow Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Lime Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Lime Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Pink Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Pink Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Gray Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Gray Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Light Gray Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Light Gray Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Cyan Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Cyan Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Purple Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Purple Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Blue Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Blue Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Brown Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Brown Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Green Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Green Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Red Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Red Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Black Glazed Terracotta",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "smelting",
				output: 1,
				recipe:["Black Terracotta","Fuel"]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "White Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["White Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Orange Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Orange Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Magenta Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Magenta Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Light Blue Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Light Blue Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Yellow Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Yellow Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Lime Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Lime Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Pink Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Pink Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Gray Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Gray Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Light Gray Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Light Gray Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Cyan Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Cyan Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Purple Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Purple Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Blue Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Blue Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Brown Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Brown Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Green Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Green Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Red Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 1,
				recipe:["Red Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Black Concrete",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "add_water",
				output: 8,
				recipe:["Black Concrete Powder",]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "White Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Bone Meal","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Orange Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Orange Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Magenta Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Magenta Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Light Blue Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Light Blue Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Yellow Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Dandelion Yellow","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Lime Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Lime Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Pink Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Pink Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Gray Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Gray Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Light Gray Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Light Gray Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Cyan Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Cyan Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Purple Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Purple Dye","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Blue Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Lapis Lazuli","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Brown Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Cocoa Beans","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Green Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Cactus Green","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Red Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Rose Red","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Black Concrete Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe:["Sand","Gravel","Sand","Gravel","Ink Sac","Gravel","Sand","Gravel","Sand"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Oak Sapling",
		minecraft_names: ["minecraft:sapling:oak"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Sapling",
		minecraft_names: ["minecraft:sapling:spruce"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Sapling",
		minecraft_names: ["minecraft:sapling:birch"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Sapling",
		minecraft_names: ["minecraft:sapling:jungle"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Sapling",
		minecraft_names: ["minecraft:sapling:acacia"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Sapling",
		minecraft_names: ["minecraft:sapling:dark_oak"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Leaves",
		minecraft_names: ["minecraft:leaves:oak"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Leaves",
		minecraft_names: ["minecraft:leaves:spruce"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Leaves",
		minecraft_names: ["minecraft:leaves:birch"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Leaves",
		minecraft_names: ["minecraft:leaves:jungle"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cobweb",
		minecraft_names: ["minecraft:web"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Grass",
		minecraft_names: ["minecraft:tallgrass:tall_grass"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Fern",
		minecraft_names: ["minecraft:tallgrass:fern"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dead Bush",
		minecraft_names: ["minecraft:deadbush"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dandelion",
		minecraft_names: ["minecraft:yellow_flower:dandelion"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Poppy",
		minecraft_names: ["minecraft:red_flower:poppy"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Orchid",
		minecraft_names: ["minecraft:red_flower:blue_orchid"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Allium",
		minecraft_names: ["minecraft:red_flower:allium"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Azure Bluet",
		minecraft_names: ["minecraft:red_flower:houstonia"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Tulip",
		minecraft_names: ["minecraft:red_flower:red_tulip"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Tulip",
		minecraft_names: ["minecraft:red_flower:orange_tulip"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Tulip",
		minecraft_names: ["minecraft:red_flower:white_tulip"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Tulip",
		minecraft_names: ["minecraft:red_flower:pink_tulip"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oxeye Daisy",
		minecraft_names: ["minecraft:red_flower:oxeye_daisy"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Mushroom",
		minecraft_names: ["minecraft:brown_mushroom"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Mushroom",
		minecraft_names: ["minecraft:red_mushroom"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Torch",
		minecraft_names: ["minecraft:torch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,"Stick",nil,nil,"Charcoal",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,"Stick",nil,nil,"Coal",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chest",
		minecraft_names: ["minecraft:chest"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks",nil,"Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks",nil,"Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks"],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Birch Wood Planks","Birch Wood Planks","Birch Wood Planks","Birch Wood Planks",nil,"Birch Wood Planks","Birch Wood Planks","Birch Wood Planks","Birch Wood Planks"],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks",nil,"Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks"],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks",nil,"Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks"],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks",nil,"Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Crafting Table",
		minecraft_names: ["minecraft:crafting_table"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks",nil,"Oak Wood Planks","Oak Wood Planks",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Spruce Wood Planks","Spruce Wood Planks",nil,"Spruce Wood Planks","Spruce Wood Planks",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Birch Wood Planks","Birch Wood Planks",nil,"Birch Wood Planks","Birch Wood Planks",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Jungle Wood Planks","Jungle Wood Planks",nil,"Jungle Wood Planks","Jungle Wood Planks",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Acacia Wood Planks","Acacia Wood Planks",nil,"Acacia Wood Planks","Acacia Wood Planks",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Dark Oak Wood Planks","Dark Oak Wood Planks",nil,"Dark Oak Wood Planks","Dark Oak Wood Planks",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Furnace",
		minecraft_names: ["minecraft:furnace", "minecraft:lit_furnace"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone","Cobblestone","Cobblestone","Cobblestone",nil,"Cobblestone","Cobblestone","Cobblestone","Cobblestone"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Ladder",
		minecraft_names: ["minecraft:ladder"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Stick",nil,"Stick","Stick","Stick","Stick","Stick",nil,"Stick"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Snow Block",
		minecraft_names: ["minecraft:snow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Snowball","Snowball",nil,"Snowball","Snowball",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cactus",
		minecraft_names: ["minecraft:cactus"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jukebox",
		minecraft_names: ["minecraft:jukebox"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Diamond","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Fence",
		minecraft_names: ["minecraft:fence"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Oak Wood Planks","Stick","Oak Wood Planks","Oak Wood Planks","Stick","Oak Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Monster Egg",
		minecraft_names: ["minecraft:monster_egg:stone"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cobblestone Monster Egg",
		minecraft_names: ["minecraft:monster_egg:cobblestone"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:stone_brick"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Mossy Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:mossy_brick"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cracked Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:cracked_brick"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chiseled Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:chiseled_brick"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Bars",
		minecraft_names: ["minecraft:iron_bars"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Glass Pane",
		minecraft_names: ["minecraft:glass_pane"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Glass","Glass","Glass","Glass","Glass","Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Vines",
		minecraft_names: ["minecraft:vine"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lily Pad",
		minecraft_names: ["minecraft:waterlily"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Brick Fence",
		minecraft_names: ["minecraft:nether_brick_fence"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Nether Brick","Nether Brick","Nether Brick","Nether Brick","Nether Brick","Nether Brick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Enchantment Table",
		minecraft_names: ["minecraft:enchanting_table"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Book",nil,"Diamond","Obsidian","Diamond","Obsidian","Obsidian","Obsidian"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "End Portal",
		minecraft_names: ["minecraft:end_portal_frame"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Ender Chest",
		minecraft_names: ["minecraft:ender_chest"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Obsidian","Obsidian","Obsidian","Obsidian","Eye of Ender","Obsidian","Obsidian","Obsidian","Obsidian"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Anvil",
		minecraft_names: ["minecraft:anvil"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Block of Iron","Block of Iron","Block of Iron",nil,"Iron Ingot",nil,"Iron Ingot","Iron Ingot","Iron Ingot"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:white"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["White Stained Glass","White Stained Glass","White Stained Glass","White Stained Glass","White Stained Glass","White Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:orange"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Orange Stained Glass","Orange Stained Glass","Orange Stained Glass","Orange Stained Glass","Orange Stained Glass","Orange Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magenta Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:magenta"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Magenta Stained Glass","Magenta Stained Glass","Magenta Stained Glass","Magenta Stained Glass","Magenta Stained Glass","Magenta Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:light_blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Light Blue Stained Glass","Light Blue Stained Glass","Light Blue Stained Glass","Light Blue Stained Glass","Light Blue Stained Glass","Light Blue Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:yellow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Yellow Stained Glass","Yellow Stained Glass","Yellow Stained Glass","Yellow Stained Glass","Yellow Stained Glass","Yellow Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:lime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Lime Stained Glass","Lime Stained Glass","Lime Stained Glass","Lime Stained Glass","Lime Stained Glass","Lime Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:pink"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Pink Stained Glass","Pink Stained Glass","Pink Stained Glass","Pink Stained Glass","Pink Stained Glass","Pink Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:gray"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Gray Stained Glass","Gray Stained Glass","Gray Stained Glass","Gray Stained Glass","Gray Stained Glass","Gray Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:silver"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Light Gray Stained Glass","Light Gray Stained Glass","Light Gray Stained Glass","Light Gray Stained Glass","Light Gray Stained Glass","Light Gray Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:cyan"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Cyan Stained Glass","Cyan Stained Glass","Cyan Stained Glass","Cyan Stained Glass","Cyan Stained Glass","Cyan Stained Glass",nil,nil,nil],
				shapeless: 0
			}
		],
	},{
		name: "Purple Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:purple"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Purple Stained Glass","Purple Stained Glass","Purple Stained Glass","Purple Stained Glass","Purple Stained Glass","Purple Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Blue Stained Glass","Blue Stained Glass","Blue Stained Glass","Blue Stained Glass","Blue Stained Glass","Blue Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:brown"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Brown Stained Glass","Brown Stained Glass","Brown Stained Glass","Brown Stained Glass","Brown Stained Glass","Brown Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:green"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Green Stained Glass","Green Stained Glass","Green Stained Glass","Green Stained Glass","Green Stained Glass","Green Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:red"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Red Stained Glass","Red Stained Glass","Red Stained Glass","Red Stained Glass","Red Stained Glass","Red Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Stained Glass Pane",
		minecraft_names: ["minecraft:stained_glass_pane:black"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Black Stained Glass","Black Stained Glass","Black Stained Glass","Black Stained Glass","Black Stained Glass","Black Stained Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Leaves",
		minecraft_names: ["minecraft:leaves2:acacia"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Leaves",
		minecraft_names: ["minecraft:leaves2:dark_oak"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Slime Block",
		minecraft_names: ["minecraft:slime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Slimeball","Slimeball","Slimeball","Slimeball","Slimeball","Slimeball","Slimeball","Slimeball","Slimeball"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Carpet",
		minecraft_names: ["minecraft:carpet:white"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Wool","Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Carpet",
		minecraft_names: ["minecraft:carpet:orange"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Orange Wool","Orange Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magenta Carpet",
		minecraft_names: ["minecraft:carpet:magenta"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Magenta Wool","Magenta Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Carpet",
		minecraft_names: ["minecraft:carpet:light_blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Light Blue Wool","Light Blue Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Carpet",
		minecraft_names: ["minecraft:carpet:yellow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Yellow Wool","Yellow Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Carpet",
		minecraft_names: ["minecraft:carpet:lime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Lime Wool","Lime Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Carpet",
		minecraft_names: ["minecraft:carpet:pink"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Pink Wool","Pink Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Carpet",
		minecraft_names: ["minecraft:carpet:gray"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Gray Wool","Gray Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Carpet",
		minecraft_names: ["minecraft:carpet:silver"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Light Gray Wool","Light Gray Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Carpet",
		minecraft_names: ["minecraft:carpet:cyan"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Cyan Wool","Cyan Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Carpet",
		minecraft_names: ["minecraft:carpet:purple"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Purple Wool","Purple Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Carpet",
		minecraft_names: ["minecraft:carpet:blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Blue Wool","Blue Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Carpet",
		minecraft_names: ["minecraft:carpet:brown"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Brown Wool","Brown Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Carpet",
		minecraft_names: ["minecraft:carpet:green"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Green Wool","Green Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Carpet",
		minecraft_names: ["minecraft:carpet:red"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Red Wool","Red Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Carpet",
		minecraft_names: ["minecraft:carpet:black"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Black Wool","Black Wool",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sunflower",
		minecraft_names: ["minecraft:double_plant:sunflower"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lilac",
		minecraft_names: ["minecraft:double_plant:syringa"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Double Tallgrass",
		minecraft_names: ["minecraft:double_plant:double_grass"], 
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Large Fern",
		minecraft_names: ["minecraft:double_plant:double_fern"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Rose Bush",
		minecraft_names: ["minecraft:double_plant:double_rose"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Peony",
		minecraft_names: ["minecraft:double_plant:paeonia"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Fence",
		minecraft_names: ["minecraft:spruce_fence"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Spruce Wood Planks","Stick","Spruce Wood Planks","Spruce Wood Planks","Stick","Spruce Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Fence",
		minecraft_names: ["minecraft:birch_fence"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Birch Wood Planks","Stick","Birch Wood Planks","Birch Wood Planks","Stick","Birch Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Fence",
		minecraft_names: ["minecraft:jungle_fence"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Jungle Wood Planks","Stick","Jungle Wood Planks","Jungle Wood Planks","Stick","Jungle Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Fence",
		minecraft_names: ["minecraft:dark_oak_fence"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Dark Oak Wood Planks","Stick","Dark Oak Wood Planks","Dark Oak Wood Planks","Stick","Dark Oak Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Fence",
		minecraft_names: ["minecraft:acacia_fence"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Acacia Wood Planks","Stick","Acacia Wood Planks","Acacia Wood Planks","Stick","Acacia Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "End Rod",
		minecraft_names: ["minecraft:end_rod"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Blaze Rod","Popped Chorus Fruit",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chorus Plant",
		minecraft_names: ["minecraft:chorus_plant"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chorus Flower",
		minecraft_names: ["minecraft:chorus_flower"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Painting",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Stick","Stick","Stick","Wool","Stick","Stick","Stick","Stick"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sign",
		minecraft_names: ["minecraft:wall_sign"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: [nil,"Stick",nil,"Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Bed",
		minecraft_names: ["minecraft:bed"], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Wool","Wool","Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Orange Wool","Orange Wool","Orange Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Orange Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "MAgenta Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Magenta Wool","Magenta Wool","Magenta Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Magenta Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Light Blue Wool","Light Blue Wool","Light Blue Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Light Blue Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Yellow Wool","Yellow Wool","Yellow Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Dandelion Yellow",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Lime Wool","Lime Wool","Lime Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Lime Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Pink Wool","Pink Wool","Pink Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Pink Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Gray Wool","Gray Wool","Gray Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Gray Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Light Gray Wool","Light Gray Wool","Light Gray Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Light Gray Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Cyan Wool","Cyan Wool","Cyan Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Cyan Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Purple Wool","Purple Wool","Purple Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Purple Dye",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Blue Wool","Blue Wool","Blue Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Lapis Lazuli",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Brown Wool","Brown Wool","Brown Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Cocoa Beans",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Green Wool","Green Wool","Green Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Cactus Green",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Red Wool","Red Wool","Red Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Rose Red",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Bed",
		minecraft_names: [], # TODO - Get correct block ID for uploader
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Black Wool","Black Wool","Black Wool",nil,nil,nil],
				shapeless: 0
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["White Bed","Ink Sac",nil,nil,nil,nil,nil,nil,nil]
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Item Frame",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Stick","Stick","Stick","Leather","Stick","Stick","Stick","Stick"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Flower Pot",
		minecraft_names: ["minecraft:flower_pot"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Brick",nil,"Brick",nil,"Brick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Skeleton Skull",
		minecraft_names: ["minecraft:skull:SkeletonSkull"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wither Skeleton Skull",
		minecraft_names: ["minecraft:skull:WitherSkeletonSkull"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Zombie Head",
		minecraft_names: ["minecraft:skull:ZombieSkull"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Head",
		minecraft_names: ["minecraft:skull:PlayerSkull"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Creeper Head",
		minecraft_names: ["minecraft:skull:CreeperSkull"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dragon Head",
		minecraft_names: ["minecraft:skull:EnderDragonSkull"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Armor Stand",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Stone Slab","Stick",nil,"Stick",nil,"Stick","Stick","Stick"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "White Banner",
		minecraft_names: ["minecraft:banner:white"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,"Wool","Wool","Wool","Wool","Wool","Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Banner",
		minecraft_names: ["minecraft:banner:orange"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Orange Wool","Orange Wool","Orange Wool","Orange Wool","Orange Wool","Orange Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magenta Banner",
		minecraft_names: ["minecraft:banner:magenta"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Magenta Wool","Magenta Wool","Magenta Wool","Magenta Wool","Magenta Wool","Magenta Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Banner",
		minecraft_names: ["minecraft:banner:light_blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Light Blue Wool","Light Blue Wool","Light Blue Wool","Light Blue Wool","Light Blue Wool","Light Blue Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Yellow Banner",
		minecraft_names: ["minecraft:banner:yellow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Yellow Wool","Yellow Wool","Yellow Wool","Yellow Wool","Yellow Wool","Yellow Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Banner",
		minecraft_names: ["minecraft:banner:lime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Lime Wool","Lime Wool","Lime Wool","Lime Wool","Lime Wool","Lime Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Banner",
		minecraft_names: ["minecraft:banner:pink"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Pink Wool","Pink Wool","Pink Wool","Pink Wool","Pink Wool","Pink Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Banner",
		minecraft_names: ["minecraft:banner:gray"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Gray Wool","Gray Wool","Gray Wool","Gray Wool","Gray Wool","Gray Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Banner",
		minecraft_names: ["minecraft:banner:silver"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Light Gray Wool","Light Gray Wool","Light Gray Wool","Light Gray Wool","Light Gray Wool","Light Gray Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Banner",
		minecraft_names: ["minecraft:banner:cyan"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Cyan Wool","Cyan Wool","Cyan Wool","Cyan Wool","Cyan Wool","Cyan Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Banner",
		minecraft_names: ["minecraft:banner:purple"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Purple Wool","Purple Wool","Purple Wool","Purple Wool","Purple Wool","Purple Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blue Banner",
		minecraft_names: ["minecraft:banner:blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Blue Wool","Blue Wool","Blue Wool","Blue Wool","Blue Wool","Blue Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brown Banner",
		minecraft_names: ["minecraft:banner:brown"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Brown Wool","Brown Wool","Brown Wool","Brown Wool","Brown Wool","Brown Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Green Banner",
		minecraft_names: ["minecraft:banner:green"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Green Wool","Green Wool","Green Wool","Green Wool","Green Wool","Green Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Red Banner",
		minecraft_names: ["minecraft:banner:red"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Red Wool","Red Wool","Red Wool","Red Wool","Red Wool","Red Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Black Banner",
		minecraft_names: ["minecraft:banner:black"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,"Black Wool","Black Wool","Black Wool","Black Wool","Black Wool","Black Wool"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "End Crystal",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Glass","Ghast Tear","Glass","Glass","Eye of Ender","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dispenser",
		minecraft_names: ["minecraft:dispenser"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone","Redstone","Cobblestone","Cobblestone","Bow","Cobblestone","Cobblestone","Cobblestone","Cobblestone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Note Block",
		minecraft_names: ["minecraft:noteblock"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Redstone","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sticky Piston",
		minecraft_names: ["minecraft:sticky_piston"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Piston",nil,nil,"Slimeball",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Piston",
		minecraft_names: ["minecraft:piston"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone","Redstone","Cobblestone","Cobblestone","Iron Ingot","Cobblestone","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource",
			}
		],
	},{
		name: "TNT",
		minecraft_names: ["minecraft:tnt"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gunpowder","Sand","Gunpowder","Sand","Gunpowder","Sand","Gunpowder","Sand","Gunpowder"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lever",
		minecraft_names: ["minecraft:lever"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone",nil,nil,"Stick",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Pressure Plate",
		minecraft_names: ["minecraft:stone_pressure_plate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stone","Stone",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Pressure Plate",
		minecraft_names: ["minecraft:wooden_pressure_plate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Redstone Torch",
		minecraft_names: ["minecraft:redstone_torch", "minecraft:unlit_redstone_torch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick",nil,nil,"Redstone",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Button",
		minecraft_names: ["minecraft:stone_button"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stone",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Trapdoor",
		minecraft_names: ["minecraft:trapdoor"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Fence Gate",
		minecraft_names: ["minecraft:fence_gate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Oak Wood Planks","Stick","Stick","Oak Wood Planks","Stick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Redstone Lamp",
		minecraft_names: ["minecraft:redstone_lamp", "minecraft:lit_redstone_lamp"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Redstone",nil,"Redstone","Glowstone","Redstone",nil,"Redstone",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Tripwire Hook",
		minecraft_names: ["minecraft:tripwire_hook"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: [nil,"Oak Wood Planks",nil,nil,"Stick",nil,nil,"Iron Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Button",
		minecraft_names: ["minecraft:wooden_button"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Trapped Chest",
		minecraft_names: ["minecraft:trapped_chest"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Chest","Tripwire Hook",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			},
		],
	},{
		name: "Weighted Pressure Plate (Light)",
		minecraft_names: ["minecraft:light_weighted_pressure_plate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Ingot","Gold Ingot",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Weighted Pressure Plate (Heavy)",
		minecraft_names: ["minecraft:heavy_weighted_pressure_plate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot","Iron Ingot",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Daylight Sensor",
		minecraft_names: ["minecraft:daylight_detector", "minecraft:daylight_detector_inverted"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Slab","Oak Wood Slab","Oak Wood Slab","Nether Quartz","Nether Quartz","Nether Quartz","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Block of Redstone",
		minecraft_names: ["minecraft:redstone_block"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Redstone","Redstone","Redstone","Redstone","Redstone","Redstone","Redstone","Redstone","Redstone"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Hopper",
		minecraft_names: ["minecraft:hopper"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Iron Ingot",nil,"Iron Ingot","Chest","Iron Ingot","Iron Ingot",nil,"Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dropper",
		minecraft_names: ["minecraft:dropper"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone","Redstone","Cobblestone","Cobblestone",nil,"Cobblestone","Cobblestone","Cobblestone","Cobblestone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Trapdoor",
		minecraft_names: ["minecraft:iron_trapdoor"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot","Iron Ingot",nil,"Iron Ingot","Iron Ingot",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Fence Gate",
		minecraft_names: ["minecraft:spruce_fence_gate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Spruce Wood Planks","Stick","Stick","Spruce Wood Planks","Stick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Fence Gate",
		minecraft_names: ["minecraft:birch_fence_gate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Birch Wood Planks","Stick","Stick","Birch Wood Planks","Stick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Fence Gate",
		minecraft_names: ["minecraft:jungle_fence_gate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Jungle Wood Planks","Stick","Stick","Jungle Wood Planks","Stick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Fence Gate",
		minecraft_names: ["minecraft:dark_oak_fence_gate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Dark Oak Wood Planks","Stick","Stick","Dark Oak Wood Planks","Stick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Fence Gate",
		minecraft_names: ["minecraft:acacia_fence_gate"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick","Acacia Wood Planks","Stick","Stick","Acacia Wood Planks","Stick",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Door",
		minecraft_names: ["minecraft:wooden_door"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Oak Wood Planks","Oak Wood Planks",nil,"Oak Wood Planks","Oak Wood Planks",nil,"Oak Wood Planks","Oak Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Door",
		minecraft_names: ["minecraft:iron_door"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Iron Ingot","Iron Ingot",nil,"Iron Ingot","Iron Ingot",nil,"Iron Ingot","Iron Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Redstone",
		minecraft_names: ["minecraft:redstone_wire"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Redstone Repeater",
		minecraft_names: ["minecraft:unpowered_repeater", "minecraft:powered_repeater"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stone","Stone","Stone","Redstone Torch","Redstone","Redstone Torch",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Redstone Comparator",
		minecraft_names: ["minecraft:unpowered_comparator"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stone","Stone","Stone","Redstone Torch","Nether Quartz","Redstone Torch",nil,"Redstone Torch",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Door",
		minecraft_names: ["minecraft:spruce_door"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Spruce Wood Planks","Spruce Wood Planks",nil,"Spruce Wood Planks","Spruce Wood Planks",nil,"Spruce Wood Planks","Spruce Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Door",
		minecraft_names: ["minecraft:birch_door"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Birch Wood Planks","Birch Wood Planks",nil,"Birch Wood Planks","Birch Wood Planks",nil,"Birch Wood Planks","Birch Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Door",
		minecraft_names: ["minecraft:jungle_door"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Jungle Wood Planks","Jungle Wood Planks",nil,"Jungle Wood Planks","Jungle Wood Planks",nil,"Jungle Wood Planks","Jungle Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Door",
		minecraft_names: ["minecraft:acacia_door"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Acacia Wood Planks","Acacia Wood Planks",nil,"Acacia Wood Planks","Acacia Wood Planks",nil,"Acacia Wood Planks","Acacia Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Door",
		minecraft_names: ["minecraft:dark_oak_door"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Dark Oak Wood Planks","Dark Oak Wood Planks",nil,"Dark Oak Wood Planks","Dark Oak Wood Planks",nil,"Dark Oak Wood Planks","Dark Oak Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Powered Rail",
		minecraft_names: ["minecraft:golden_rail"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Gold Ingot","Redstone","Gold Ingot","Gold Ingot","Stick","Gold Ingot","Gold Ingot",nil,"Gold Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Detector Rail",
		minecraft_names: ["minecraft:detector_rail"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Iron Ingot","Redstone","Iron Ingot","Iron Ingot","Stone Pressure Plate","Iron Ingot","Iron Ingot",nil,"Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Rail",
		minecraft_names: ["minecraft:rail"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 16,
				recipe: ["Iron Ingot",nil,"Iron Ingot","Iron Ingot","Stick","Iron Ingot","Iron Ingot",nil,"Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Activator Rail",
		minecraft_names: ["minecraft:activator_rail"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 6,
				recipe: ["Iron Ingot","Stick","Iron Ingot","Iron Ingot","Redstone Torch","Iron Ingot","Iron Ingot","Stick","Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Minecart",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot",nil,"Iron Ingot",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Saddle",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Oak Boat",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks",nil,"Oak Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Minecart with Chest",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Minecart",nil,nil,"Chest",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Minecart with Furnace",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Minecart",nil,nil,"Furnace",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Carrot on a Stick",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Carrot",nil,"Fishing Rod",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Minecart with TNT",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Minecart",nil,nil,"TNT",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Minecart with Hopper",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Minecart",nil,nil,"Hopper",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Elytra",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spruce Boat",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks","Spruce Wood Planks",nil,"Spruce Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Birch Boat",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Birch Wood Planks","Birch Wood Planks","Birch Wood Planks","Birch Wood Planks",nil,"Birch Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Jungle Boat",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks","Jungle Wood Planks",nil,"Jungle Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Acacia Boat",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks","Acacia Wood Planks",nil,"Acacia Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dark Oak Boat",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks","Dark Oak Wood Planks",nil,"Dark Oak Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Totem of Undying",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Shulker Shell",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Beacon",
		minecraft_names: ["minecraft:beacon"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Obsidian","Obsidian","Obsidian","Glass","Nether Star","Glass","Glass","Glass","Glass"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bucket",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Iron Ingot",nil,"Iron Ingot",nil,"Iron Ingot",nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Water Bucket",
		minecraft_names: ["minecraft:water"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lava Bucket",
		minecraft_names: ["minecraft:lava"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Snowball",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Milk",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Paper",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Sugar Canes","Sugar Canes","Sugar Canes",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Book",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Paper","Leather","Paper","Paper",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Slimeball",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				output: 9,
				recipe_type: "crafting",
				recipe: [nil,nil,nil,nil,"Slime Block",nil,nil,nil,nil],
				shapeless: 0
			}
		],
	},{
		name: "Bone",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Ender Pearl",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Eye of Ender",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Blaze Powder","Ender Pearl",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Fire Charge",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Gunpowder",nil,"Blaze Powder","Charcoal",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Book and Quill",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Feather",nil,"Book","Ink Sac",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Empty Map",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Paper","Paper","Paper","Paper","Compass","Paper","Paper","Paper","Paper"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Firework Star",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Horse Armor",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gold Horse Armor",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Horse Armor",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Apple",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Mushroom Stew",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Red Mushroom","Brown Mushroom","Bowl",nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bread",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wheat","Wheat","Wheat",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Raw Porkchop",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cooked Porkchop",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Apple",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Apple","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Notch Apple",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Raw Fish",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Raw Salmon",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Clownfish",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pufferfish",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cooked Fish",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Raw Fish", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cooked Salmon",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Raw Salmon", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cake",
		minecraft_names: ["minecraft:cake"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wheat","Wheat","Wheat","Sugar","Egg","Sugar","Milk","Milk","Milk"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cookie",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Wheat","Cocoa Beans","Wheat",nil,nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Melon Slice",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Raw Beef",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Steak",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Raw Fish", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Raw Chicken",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cooked Chicken",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Raw Chicken", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Rotten Flesh",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spider Eye",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Carrot",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Potato",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Baked Potato",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Poisonous Potato",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pumpkin Pie",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Pumpkin","Sugar","Egg",nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Raw Rabbit",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cooked Rabbit",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Raw Rabbit", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Rabbit Stew",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Bowl",nil,"Carrot","Baked Potato","Brown Mushroom",nil,"Cooked Rabbit",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Raw Mutton",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cooked Mutton",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Raw Mutton", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Beetroot",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Beetroot Soup",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Bowl",nil,"Beetroot","Beetroot","Beetroot","Beetroot","Beetroot","Beetroot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Shovel",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Iron Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Pickaxe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,"Iron Ingot","Iron Ingot","Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Axe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick","Iron Ingot",nil,"Iron Ingot","Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Flint and Steel",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Flint",nil,"Iron Ingot",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Shovel",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Oak Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Pickaxe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,"Oak Wood Planks","Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Axe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick","Oak Wood Planks",nil,"Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Shovel",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Cobblestone",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Pickaxe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,"Cobblestone","Cobblestone","Cobblestone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Axe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick","Cobblestone",nil,"Cobblestone","Cobblestone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Shovel",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Diamond",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Pickaxe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,"Diamond","Diamond","Diamond"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Axe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick","Diamond",nil,"Diamond","Diamond"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Shovel",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Gold Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Pickaxe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,"Gold Ingot","Gold Ingot","Gold Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Axe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick","Gold Ingot",nil,"Gold Ingot","Gold Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Hoe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Oak Wood Planks","Oak Wood Planks"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Hoe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Cobblestone","Cobblestone"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Hoe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Iron Ingot","Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Hoe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Diamond","Diamond"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Hoe",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Stick",nil,nil,"Gold Ingot","Gold Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Compass",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Iron Ingot",nil,"Iron Ingot","Redstone","Iron Ingot",nil,"Iron Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Fishing Rod",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick",nil,"String",nil,"Stick","String",nil,nil,"Stick"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Clock",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Gold Ingot",nil,"Gold Ingot","Redstone","Gold Ingot",nil,"Gold Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Shears",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot",nil,nil,"Iron Ingot",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lead",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,"String","String","Slimeball",nil,"String","String",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Name Tag",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bow",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["String","Stick",nil,"String",nil,"Stick","String","Stick",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Arrow",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,"Feather",nil,nil,"Stick",nil,nil,"Flint",nil],
				shapeless: 0
			},

		],
	},{
		name: "Iron Sword",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Iron Ingot",nil,nil,"Iron Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wooden Sword",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Oak Wood Planks",nil,nil,"Oak Wood Planks",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Stone Sword",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Cobblestone",nil,nil,"Cobblestone",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Sword",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Diamond",nil,nil,"Diamond",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Sword",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Stick",nil,nil,"Gold Ingot",nil,nil,"Gold Ingot",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Leather Cap",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Leather",nil,"Leather","Leather","Leather","Leather",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Leather Tunic",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Leather","Leather","Leather","Leather","Leather","Leather","Leather",nil,"Leather"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Leather Pants",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Leather",nil,"Leather","Leather",nil,"Leather","Leather","Leather","Leather"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Leather Boots",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Leather",nil,"Leather","Leather",nil,"Leather",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chain Helmet",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chain Chestplate",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chain Leggings",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chain Boots",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Helmet",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot",nil,"Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Chestplate",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot",nil,"Iron Ingot"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Leggings",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot",nil,"Iron Ingot","Iron Ingot",nil,"Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Boots",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot",nil,"Iron Ingot","Iron Ingot",nil,"Iron Ingot",nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Helmet",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Diamond",nil,"Diamond","Diamond","Diamond","Diamond",nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Chestplate",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Diamond","Diamond","Diamond","Diamond","Diamond","Diamond","Diamond",nil,"Diamond"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Leggings",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Diamond",nil,"Diamond","Diamond",nil,"Diamond","Diamond","Diamond","Diamond"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond Boots",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Diamond",nil,"Diamond","Diamond",nil,"Diamond",nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Helmet",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Ingot",nil,"Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot",nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Chestplate",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot",nil,"Gold Ingot"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Leggings",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Ingot",nil,"Gold Ingot","Gold Ingot",nil,"Gold Ingot","Gold Ingot","Gold Ingot","Gold Ingot"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Boots",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Ingot",nil,"Gold Ingot","Gold Ingot",nil,"Gold Ingot",nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Spectral Arrow",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: [nil,"Glowstone Dust",nil,"Glowstone Dust","Arrow","Glowstone Dust",nil,"Glowstone Dust",nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Shield",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Oak Wood Planks",nil,"Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Iron Ingot","Oak Wood Planks"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Ghast Tear",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Water Bottle",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Glass Bottle",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: [nil,"Glass",nil,"Glass",nil,"Glass",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Fermented Spider Eye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Brown Mushroom","Sugar","Spider Eye",nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blaze Powder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Blaze Rod",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magma Cream",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Blaze Powder","Slimeball",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brewing Stand",
		minecraft_names: ["minecraft:brewing_stand"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone","Cobblestone","Cobblestone",nil,"Blaze Rod",nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cauldron",
		minecraft_names: ["minecraft:cauldron"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Iron Ingot","Iron Ingot","Iron Ingot","Iron Ingot",nil,"Iron Ingot","Iron Ingot",nil,"Iron Ingot"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Glistering Melon",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget","Melon Slice","Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget"],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Golden Carrot",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget","Carrot","Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget"],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Rabbit's Foot",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dragon's Breath",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Coal",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Charcoal",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Oak Wood", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Diamond",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Iron Ingot",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				output: 9,
				recipe:[nil,nil,nil,nil,"Block of Iron",nil,nil,nil,nil],
				recipe_type: "crafting",
				shapeless: 1
			},
			{
				output: 9,
				recipe:["Iron Nugget","Iron Nugget","Iron Nugget","Iron Nugget","Iron Nugget","Iron Nugget","Iron Nugget","Iron Nugget","Iron Nugget"],
				recipe_type: "crafting",
				shapeless: 1
			}
		],
	},{
		name: "Gold Ingot",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				recipe_type: "crafting",
				output: 9,
				recipe: [nil,nil,nil,nil,"Block of Gold",nil,nil,nil,nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget","Gold Nugget"],
				shapeless: 1
			}
		],
	},{
		name: "Stick",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Oak Wood Planks",nil,nil,"Oak Wood Planks",nil,nil,nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bowl",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,"Oak Wood Planks",nil,"Oak Wood Planks",nil,"Oak Wood Planks",nil,nil,nil],
				shapeless: 0
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "String",
		minecraft_names: ["minecraft:tripwire"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Feather",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gunpowder",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Seeds",
		minecraft_names: ["minecraft:wheat"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Wheat",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Flint",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Leather",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Brick",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Clay", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Clay",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sugar Canes",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Egg",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Glowstone Dust",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Ink Sac",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Rose Red",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Poppy",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cactus Green",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cocoa Beans",
		minecraft_names: ["minecraft:cocoa"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lapis Lazuli",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Purple Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Lapis Lazuli","Rose Red",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Cyan Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Lapis Lazuli","Cactus Green",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Gray Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Bone Meal","Bone Meal","Ink Sac",nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gray Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Bone Meal","Ink Sac",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pink Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Bone Meal","Rose Red",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Lime Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Cactus Green","Bone Meal",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Dandelion Yellow",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Dandelion",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Light Blue Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Lapis Lazuli","Bone Meal",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Magenta Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Rose Red","Rose Red","Lapis Lazuli","Bone Meal",nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Orange Dye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 2,
				recipe: ["Dandelion Yellow","Rose Red",nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Bone Meal",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: ["Bone",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 9,
				recipe: ["Bone Block",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Sugar",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Sugar Canes",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Pumpkin Seeds",
		minecraft_names: ["minecraft:pumpkin_stem"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: ["Pumpkin",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Melon Seeds",
		minecraft_names: ["minecraft:melon_stem"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Melon Slice",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Blaze Rod",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Gold Nugget",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 9,
				recipe: ["Gold Ingot",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Helmet", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Chestplate", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Leggings", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Boots", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Sword", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Hoe", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Axe", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Golden Pickaxe", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Gold Horse Armor", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Wart",
		minecraft_names: ["minecraft:nether_wart"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Emerald",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			},
			{
				recipe_type: "crafting",
				output: 9,
				recipe: ["Emerald Block",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},

		],
	},{
		name: "Nether Star",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Brick",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Nether Quartz",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Prismarine Shard",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Prismarine Crystals",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Rabbit Hide",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Chorus Fruit",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		],
	},{
		name: "Popped Chorus Fruit",
		minecraft_names: [],
		recipes: [
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Chorus Fruit", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Beetroot Seeds",
		minecraft_names: ["minecraft:beetroots"],
		recipes: [
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Iron Nugget",
		minecraft_names: [],
		recipes: [

			{
				recipe_type: "crafting",
				output: 9,
				recipe: ["Iron Ingot",nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Helmet", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Chestplate", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Leggings", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Boots", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Sword", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Hoe", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Axe", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Pickaxe", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "smelting",
				recipe: ["Iron Horse Armor", "Fuel"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Firework",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 3,
				recipe: [nil,nil,nil,nil,"Paper",nil,"Gunpowder","Gunpowder","Gunpowder"],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 3,
				recipe: [nil,nil,nil,nil,"Paper",nil,"Gunpowder","Gunpowder",nil],
				shapeless: 1
			},
			{
				recipe_type: "crafting",
				output: 3,
				recipe: [nil,nil,nil,nil,"Paper",nil,nil,"Gunpowder",nil],
				shapeless: 1
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	},{
		name: "Fuel",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "as",
				output: 8,
				recipe: ["Coal"],
			},
			{
				recipe_type: "as",
				output: 8,
				recipe: ["Charcoal"],
			},
			{
				recipe_type: "as",
				output: 80,
				recipe: ["Block of Coal"],
			},
			{
				recipe_type: "as",
				output: 100,
				recipe: ["Lava Bucket"],
			},
			{
				recipe_type: "as",
				output: 12,
				recipe: ["Blaze Rod"],
			},
			{
				recipe_type: "as",
				output: 1,
				recipe: ["Stick", "Stick"],
			},
			{
				output: 1,
				recipe_type: "raw_resource"
			}
		]
	}


	# a map of property names to weather they should be included in the item lookup
	@object_properties = {
		axis: false,
		variant: true,
		powered: false,
		facing: false,
		type: true,
		check_decay: false,
		decayable: false,
		explode: false,
		color: true,
		wet: true,
		snowy: false,
		rotation: false,
		mode: false,
		nodrop: false,
		legacy_data: false,
		contents: false,
		has_bottle_2: false,
		has_bottle_1: false,
		has_bottle_0: false,
		has_record: false,
		triggered: false,
		enabled: false,
		power: false,
		age: false,
		open: false,
		hinge: false,
		half: false,
		locked: false,
		delay: false,
		occupied: false,
		part: false,
		bites: false,
		level: false,
		moisture: false,
		disarmed: false,
		attached: false,
		south: false,
		north: false,
		east: false,
		west: false,
		shape: false,
		down: false,
		up: false,
		in_wall: false,
		layers: false,
		extended: false,
		damage: false,
		eye: false,
		stage: false
	}





	def self.recipe_count
		count = 0
		for recipe in @minecraft_recipes
			count += 1
		end
		return count
	end

	def self.item_list
		output_list = {}
		for item in @minecraft_recipes
			name = item[:name]
			recipes = item[:recipes]

			for recipe in recipes


				required_resources = Hash.new(0)

				if (recipe[:recipe_type] == "raw_resource")
					# Create a dummy value that will show up for recipe selection
					# but will not effect the overall crafting calculation
					required_resources[name] = 0
				else
					# iterate over the array, counting duplicate entries
					recipe[:recipe].each do |recipe_item|
						if (recipe_item != nil)
							required_resources[recipe_item] -= 1
						end
					end
				end
				recipe[:requirements] = required_resources
			end


			output_list[name] = recipes
		end
		return output_list
	end


	def self.styles
		return {
			menu_background_color: "C3C3C3",
			menu_border_image: "FrameBorder.png",
			menu_border_width: 10,

			item_width: 32,
			item_hight: 32,
			inset_background_color: "8b8b8b",
			inset_border_image: "ItemBorder.png",
			inset_border_width: 2,

			custom_css: '/* @font-face kit by Fonts2u (http://www.fonts2u.com) */ @font-face {font-family:"Minecraft Regular";src:url("minecraft_font_by_pwnage_block-d37t6nb.eot?") format("eot"),url("minecraft_font_by_pwnage_block-d37t6nb.woff") format("woff"),url("minecraft_font_by_pwnage_block-d37t6nb.ttf") format("truetype"),url("minecraft_font_by_pwnage_block-d37t6nb.svg#Minecraft") format("svg");font-weight:normal;font-style:normal;}',
			font_family: "'Minecraft Regular', courier, sans-serif",
			# font_size:
			# font_weight:


			use_minecraft_customs: true,
		}
	end

	# Generate a name mapping for use when importing, maps the raw game-names to
	# the resource calculator readable ids
	def self.minecraft_name_map
		mapping_list = {}

		for recipe in @minecraft_recipes
			for minecraft_name in recipe[:minecraft_names]
				mapping_list[minecraft_name] = recipe[:name]
			end
		end
		return mapping_list
	end


	def self.property_map
		return @object_properties
	end
end
