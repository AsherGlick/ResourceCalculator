# This is designed as a reverse recipe lookup validator for the main recipe list
# for anything to do with the stonecutter. This is because it is easy to put a
# block in the stonecutter in-game and see all the things it can be cut into
# so it is easy to build a complete list of things that can be cut out of other
# blocks. This will then take that list and make sure those other blocks do 
# have recipes that include each of these source blocks.

stonecutter_results = {
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
		"Polished Andedsite Slab",
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
		"Red nether Brick Wall",
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


