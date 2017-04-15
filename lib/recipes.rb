module Recipes

	@minecraft_recipes = {
		name: "Stone",
		minecraft_names: ["minecraft:stone:stone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Grass Block",
		minecraft_names: ["minecraft:grass", "minecraft:grass_path"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dirt",
		minecraft_names: ["minecraft:dirt:dirt", "minecraft:farmland"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
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
			}
		],
	},{
		name: "Podzol",
		minecraft_names: ["minecraft:dirt:podzol"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cobblestone",
		minecraft_names: ["minecraft:cobblestone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Bedrock",
		minecraft_names: ["minecraft:bedrock"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Sand",
		minecraft_names: ["minecraft:sand:sand"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Red Sand",
		minecraft_names: ["minecraft:sand:red_sand"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Gravel",
		minecraft_names: ["minecraft:gravel"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Gold Ore",
		minecraft_names: ["minecraft:gold_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Iron Ore",
		minecraft_names: ["minecraft:iron_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Coal Ore",
		minecraft_names: ["minecraft:coal_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Oak Wood",
		minecraft_names: ["minecraft:log:oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Spruce Wood",
		minecraft_names: ["minecraft:log:spruce"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Birch Wood",
		minecraft_names: ["minecraft:log:birch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Jungle Wood",
		minecraft_names: ["minecraft:log:jungle"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Sponge",
		minecraft_names: ["minecraft:sponge:false"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Wet Sponge",
		minecraft_names: ["minecraft:sponge:true"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Glass",
		minecraft_names: ["minecraft:glass"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Lapis Lazuli Ore",
		minecraft_names: ["minecraft:lapis_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Orange Wool",
		minecraft_names: ["minecraft:wool:orange"],
		recipes: [
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
			}
		],
	},{
		name: "Obsidian",
		minecraft_names: ["minecraft:obsidian"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Diamond Ore",
		minecraft_names: ["minecraft:diamond_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Redstone Ore",
		minecraft_names: ["minecraft:lit_redstone_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Ice",
		minecraft_names: ["minecraft:ice"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Snow",
		minecraft_names: ["minecraft:snow_layer"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Clay",
		minecraft_names: ["minecraft:clay"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Pumpkin",
		minecraft_names: ["minecraft:pumpkin"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Netherrack",
		minecraft_names: ["minecraft:netherrack"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Soul Sand",
		minecraft_names: ["minecraft:soul_sand"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Cracked Stone Bricks",
		minecraft_names: ["minecraft:stonebrick:cracked_stonebrick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Mycelium",
		minecraft_names: ["minecraft:mycelium"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "End Stone",
		minecraft_names: ["minecraft:end_stone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Emerald Ore",
		minecraft_names: ["minecraft:emerald_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Nether Quartz Ore",
		minecraft_names: ["minecraft:quartz_ore"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "White Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:white"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Bone Meal","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Orange Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:orange"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Orange Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Magenta Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:magenta"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Magenta Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Light Blue Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:light_blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Light Blue Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Yellow Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:yellow"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Dandelion Yellow","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Lime Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:lime"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Lime Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Pink Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:pink"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Pink Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Gray Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:gray"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Gray Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Light Gray Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:silver"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Light Gray Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Cyan Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:cyan"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Cyan Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Purple Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:purple"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Purple Dye","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Blue Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:blue"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Lapis Lazuli","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Brown Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:brown"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Cocoa Beans","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Green Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:green"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Cactus Green","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Red Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:red"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Rose Red","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Black Hardened Clay",
		minecraft_names: ["minecraft:stained_hardened_clay:black"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 8,
				recipe: ["Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay","Ink Sac","Hardened Clay","Hardened Clay","Hardened Clay","Hardened Clay"],
				shapeless: 0
			}
		],
	},{
		name: "Acacia Wood",
		minecraft_names: ["minecraft:log2:acacia"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dark Oak Wood",
		minecraft_names: ["minecraft:log2:dark_oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Hardened Clay",
		minecraft_names: ["minecraft:hardened_clay"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Packed Ice",
		minecraft_names: ["minecraft:packed_ice"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Oak Sapling",
		minecraft_names: ["minecraft:sapling:oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Spruce Sapling",
		minecraft_names: ["minecraft:sapling:spruce"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Birch Sapling",
		minecraft_names: ["minecraft:sapling:birch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Jungle Sapling",
		minecraft_names: ["minecraft:sapling:jungle"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Acacia Sapling",
		minecraft_names: ["minecraft:sapling:acacia"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dark Oak Sapling",
		minecraft_names: ["minecraft:sapling:dark_oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Oak Leaves",
		minecraft_names: ["minecraft:leaves:oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Spruce Leaves",
		minecraft_names: ["minecraft:leaves:spruce"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Birch Leaves",
		minecraft_names: ["minecraft:leaves:birch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Jungle Leaves",
		minecraft_names: ["minecraft:leaves:jungle"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cobweb",
		minecraft_names: ["minecraft:web"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Grass",
		minecraft_names: ["minecraft:tallgrass:tall_grass"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Fern",
		minecraft_names: ["minecraft:tallgrass:fern"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dead Bush",
		minecraft_names: ["minecraft:deadbush"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dandelion",
		minecraft_names: ["minecraft:yellow_flower:dandelion"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Poppy",
		minecraft_names: ["minecraft:red_flower:poppy"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Blue Orchid",
		minecraft_names: ["minecraft:red_flower:blue_orchid"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Allium",
		minecraft_names: ["minecraft:red_flower:allium"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Azure Bluet",
		minecraft_names: ["minecraft:red_flower:houstonia"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Red Tulip",
		minecraft_names: ["minecraft:red_flower:red_tulip"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Orange Tulip",
		minecraft_names: ["minecraft:red_flower:orange_tulip"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "White Tulip",
		minecraft_names: ["minecraft:red_flower:white_tulip"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Pink Tulip",
		minecraft_names: ["minecraft:red_flower:pink_tulip"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Oxeye Daisy",
		minecraft_names: ["minecraft:red_flower:oxeye_daisy"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Brown Mushroom",
		minecraft_names: ["minecraft:brown_mushroom"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Red Mushroom",
		minecraft_names: ["minecraft:red_mushroom"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Furnace",
		minecraft_names: ["minecraft:furnace"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Cobblestone","Cobblestone","Cobblestone","Cobblestone",nil,"Cobblestone","Cobblestone","Cobblestone","Cobblestone"],
				shapeless: 1
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
			}
		],
	},{
		name: "Cactus",
		minecraft_names: ["minecraft:cactus"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Stone Monster Egg",
		minecraft_names: ["minecraft:monster_egg:stone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cobblestone Monster Egg",
		minecraft_names: ["minecraft:monster_egg:cobblestone"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:stone_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Mossy Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:mossy_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cracked Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:cracked_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Chiseled Stone Brick Monster Egg",
		minecraft_names: ["minecraft:monster_egg:chiseled_brick"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Vines",
		minecraft_names: ["minecraft:vine"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Lily Pad",
		minecraft_names: ["minecraft:waterlily"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "End Portal",
		minecraft_names: ["minecraft:end_portal_frame"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Acacia Leaves",
		minecraft_names: ["minecraft:leaves2:acacia"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dark Oak Leaves",
		minecraft_names: ["minecraft:leaves2:dark_oak"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Sunflower",
		minecraft_names: ["minecraft:double_plant:sunflower"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Lilac",
		minecraft_names: ["minecraft:double_plant:syringa"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Double Tallgrass",
		minecraft_names: ["minecraft:double_plant:double_grass"], 
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Large Fern",
		minecraft_names: ["minecraft:double_plant:double_fern"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Rose Bush",
		minecraft_names: ["minecraft:double_plant:double_rose"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Peony",
		minecraft_names: ["minecraft:double_plant:paeonia"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Chorus Plant",
		minecraft_names: ["minecraft:chorus_plant"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Chorus Flower",
		minecraft_names: ["minecraft:chorus_flower"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Bed",
		minecraft_names: ["minecraft:bed"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Planks","Oak Wood Planks","Oak Wood Planks","Wool","Wool","Wool",nil,nil,nil],
				shapeless: 0
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
			}
		],
	},{
		name: "Skeleton Skull",
		minecraft_names: ["minecraft:skull:SkeletonSkull"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Wither Skeleton Skull",
		minecraft_names: ["minecraft:skull:WitherSkeletonSkull"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Zombie Head",
		minecraft_names: ["minecraft:skull:ZombieSkull"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Head",
		minecraft_names: ["minecraft:skull:PlayerSkull"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Creeper Head",
		minecraft_names: ["minecraft:skull:CreeperSkull"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dragon Head",
		minecraft_names: ["minecraft:skull:EnderDragonSkull"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Redstone Torch",
		minecraft_names: ["minecraft:redstone_torch"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stick",nil,nil,"Redstone",nil,nil,nil,nil,nil],
				shapeless: 0
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
			}
		],
	},{
		name: "Redstone Lamp",
		minecraft_names: ["minecraft:redstone_lamp"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,"Redstone",nil,"Redstone","Glowstone","Redstone",nil,"Redstone",nil],
				shapeless: 0
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
			}
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
			}
		],
	},{
		name: "Daylight Sensor",
		minecraft_names: ["minecraft:daylight_detector"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Oak Wood Slab","Oak Wood Slab","Oak Wood Slab","Nether Quartz","Nether Quartz","Nether Quartz","Glass","Glass","Glass"],
				shapeless: 0
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
			}
		],
	},{
		name: "Redstone",
		minecraft_names: ["minecraft:redstone_wire"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Redstone Repeater",
		minecraft_names: ["minecraft:unpowered_repeater"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: ["Stone","Stone","Stone","Redstone Torch","Redstone","Redstone Torch",nil,nil,nil],
				shapeless: 0
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
			}
		],
	},{
		name: "Saddle",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Elytra",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Totem of Undying",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Shulker Shell",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Water Bucket",
		minecraft_names: ["minecraft:water"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Lava Bucket",
		minecraft_names: ["minecraft:lava"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Snowball",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Milk",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Slimeball",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 0
			}
		],
	},{
		name: "Bone",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Ender Pearl",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Firework Star",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Iron Horse Armor",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Gold Horse Armor",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Diamond Horse Armor",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Apple",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Raw Porkchop",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cooked Porkchop",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Notch Apple",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Raw Fish",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Raw Salmon",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Clownfish",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Pufferfish",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cooked Fish",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cooked Salmon",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Melon Slice",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Raw Beef",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Steak",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Raw Chicken",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cooked Chicken",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Rotten Flesh",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Spider Eye",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Carrot",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Potato",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Baked Potato",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Poisonous Potato",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Raw Rabbit",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cooked Rabbit",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Raw Mutton",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cooked Mutton",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Beetroot",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Name Tag",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Arrow",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 4,
				recipe: [nil,"Feather",nil,nil,"Stick",nil,nil,"Flint",nil],
				shapeless: 0
			}
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
			}
		],
	},{
		name: "Chain Helmet",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Chain Chestplate",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Chain Leggings",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Chain Boots",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Ghast Tear",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Water Bottle",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Rabbit's Foot",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Dragon's Breath",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Coal",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Charcoal",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Diamond",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Iron Ingot",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Gold Ingot",
		minecraft_names: [],
		recipes: [
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
			}
		],
	},{
		name: "String",
		minecraft_names: ["minecraft:tripwire"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Feather",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Gunpowder",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Seeds",
		minecraft_names: ["minecraft:wheat"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Wheat",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Flint",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Leather",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Brick",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Clay",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Sugar Canes",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Egg",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Glowstone Dust",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Ink Sac",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Cactus Green",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Cocoa Beans",
		minecraft_names: ["minecraft:cocoa"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Lapis Lazuli",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
			}
		],
	},{
		name: "Blaze Rod",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Gold Nugget",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Nether Wart",
		minecraft_names: ["minecraft:nether_wart"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Emerald",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Nether Star",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Nether Brick",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Nether Quartz",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Prismarine Shard",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Prismarine Crystals",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Rabbit Hide",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Chorus Fruit",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		],
	},{
		name: "Popped Chorus Fruit",
		minecraft_names: [],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
			}
		]
	},{
		name: "Beetroot Seeds",
		minecraft_names: ["minecraft:beetroots"],
		recipes: [
			{
				recipe_type: "crafting",
				output: 1,
				recipe: [nil,nil,nil,nil,nil,nil,nil,nil,nil],
				shapeless: 1
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
		for recipe in @minecraft_recipes
			name = recipe[:name]
			recipes = recipe[:recipes]

			output_list[name] = recipes
		end
		return output_list
	end

	# def recipie_graph
	# end

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