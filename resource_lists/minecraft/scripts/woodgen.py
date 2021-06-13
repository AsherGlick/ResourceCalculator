wood_types = [
    "Oak",
    "Spruce",
    "Birch",
    "Jungle",
    "Acacia",
    "Dark Oak",
]
nether_wood_types = [
    "Crimson",
    "Warped",
]
all_wood_types = wood_types + nether_wood_types

chunk = []
def indent_print(string):
    global chunk
    chunk.append(string)

def print_chunk():
    global chunk
    for string in chunk:
        print("  "+string)
    print("")
    chunk=[]


replacements = {}
def mrep(string):
    if string in replacements:
        return replacements[string]
    return string


################################################################################
# Generates all of the wood plank types
################################################################################
def planks():
    for wood_type in wood_types:
        indent_print(mrep(wood_type + " Planks") + ":")
        indent_print("  recipes:")
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Log".format(wood_type))))
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("Stripped {} Log".format(wood_type))))
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Wood".format(wood_type))))
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format("Stripped {} Wood".format(wood_type)))
        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

    for wood_type in nether_wood_types:
        indent_print(mrep(wood_type+ " Planks") + ":")
        indent_print("  recipes:")        
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Stem".format(wood_type))))
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("Stripped {} Stem".format(wood_type))))
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Hyphae".format(wood_type))))
        indent_print("  - output: 4")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("Stripped {} Hyphae".format(wood_type))))
        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def logs():
    for wood_type in wood_types:
        indent_print(mrep(wood_type + " Log") + ":")
        indent_print("  recipes:")
        indent_print("  - recipe_type: Raw Resource")
        print_chunk()
    for wood_type in nether_wood_types:
        indent_print(mrep(wood_type + " Stem") + ":")
        indent_print("  recipes:")
        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

    for wood_type in wood_types:
        indent_print(mrep("Stripped " + wood_type + " Log") + ":")
        indent_print("  recipes:")
        indent_print("  - output: 1")
        indent_print("    recipe_type: Strip")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Log".format(wood_type))))
        indent_print("  - recipe_type: Raw Resource")
        print_chunk()
    for wood_type in nether_wood_types:
        indent_print(mrep("Stripped " + wood_type + " Stem") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 1")
        indent_print("    recipe_type: Strip")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Stem".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

################################################################################
################################################################################
################################################################################
def wood():
    for wood_type in wood_types:
        indent_print(mrep("Stripped " + wood_type + " Wood") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 1")
        indent_print("    recipe_type: Strip")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Wood".format(wood_type))))

        indent_print("  - output: 3")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -4".format(mrep("Stripped {} Log".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

    for wood_type in nether_wood_types:
        indent_print(mrep("Stripped " + wood_type + " Hyphae") + ":")
        indent_print("  recipes:")
        
        indent_print("  - output: 1")
        indent_print("    recipe_type: Strip")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Stem".format(wood_type))))

        indent_print("  - output: 3")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -4".format(mrep("Stripped {} Stem".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

    for wood_type in wood_types:
        indent_print(mrep(wood_type + " Wood") + ":")
        indent_print("  recipes:")
        
        indent_print("  - output: 3")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -4".format(mrep("{} Log".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

    for wood_type in nether_wood_types:
        indent_print(mrep(wood_type + " Hyphae") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 3")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -4".format(mrep("{} Stem".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()



################################################################################
################################################################################
################################################################################
def slab():
    for wood_type in all_wood_types:
        indent_print(mrep(wood_type + " Slab") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 6")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -3".format(mrep("{} Planks".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()


def fence():
    for wood_type in all_wood_types:
        indent_print(mrep(wood_type + " Fence") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 3")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -4".format(mrep("{} Planks".format(wood_type))))
        indent_print("      Stick: -2")

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def button():
    for wood_type in all_wood_types:

        indent_print(mrep(wood_type + " Button") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 1")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -1".format(mrep("{} Planks".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def pressure_plate():
    for wood_type in all_wood_types:

        indent_print(mrep(wood_type + " Pressure Plate") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 1")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -2".format(mrep("{} Planks".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def door():
    for wood_type in all_wood_types:

        indent_print(mrep(wood_type + " Door") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 3")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -6".format(mrep("{} Planks".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def trapdoor():
    for wood_type in all_wood_types:

        indent_print(mrep(wood_type + " Trapdoor") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 2")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -6".format(mrep("{} Planks".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def fencegate():
    for wood_type in all_wood_types:

        indent_print(mrep(wood_type + " Fence Gate") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 2")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      Stick: -4")
        indent_print("      {}: -2".format(mrep("{} Planks".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def boat():
    for wood_type in wood_types:
        indent_print(mrep(wood_type + " Boat") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 1")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -5".format(mrep("{} Planks".format(wood_type))))

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

def sign():
    for wood_type in all_wood_types:

        indent_print(mrep(wood_type + " Sign") + ":")
        indent_print("  recipes:")

        indent_print("  - output: 3")
        indent_print("    recipe_type: Crafting")
        indent_print("    requirements:")
        indent_print("      {}: -6".format(mrep("{} Planks".format(wood_type))))
        indent_print("      Stick: -1")

        indent_print("  - recipe_type: Raw Resource")
        print_chunk()

# planks()

# logs()
# wood()
# slab()

# fence()

# button()
# pressure_plate()
# door()
# trapdoor()

# fencegate()
# boat()

sign()