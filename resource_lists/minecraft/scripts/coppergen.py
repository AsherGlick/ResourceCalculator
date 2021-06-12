oxidization_levels = [
    "",
    "Exposed ",
    "Weathered ",
    "Oxidized ",
]
replacements = {
    "Copper": "Block of Copper",
    "Waxed Copper": "Waxed Block of Copper",
}


items = [
    "Copper",
    "Cut Copper",
    "Cut Copper Stairs",
    "Cut Copper Slab",
]

waxed_states = [
    "",
    "Waxed ",
]


chunk = []
def indent_print(string):
    global chunk
    chunk.append(string)

def print_chunk():
    global chunk

    # autogen_comment = "# Generated with coppergen.py"

    # max_length = max([len(x) for x in chunk] + [len(autogen_comment)+2])

    # trail_length = (max_length - len(autogen_comment)+2)


    # trail = " #" * int(trail_length / 2)

    # if trail_length%2 == 1:
    #     trail = " " + trail

    # print ("  "+autogen_comment+trail)

    for string in chunk:
        # print("  "+string.ljust(max_length+1) + "#")
        print("  "+string)
    print("")
    chunk=[]

def mrep(string):
    if string in replacements:
        return replacements[string]
    return string

for waxed in waxed_states:
    for item in items:
        for oxidization_level in range(len(oxidization_levels)):
            oxidization = oxidization_levels[oxidization_level]

            if mrep(waxed + oxidization + item) == "Block of Copper":
                continue
            indent_print(mrep(waxed + oxidization + item) + ":")
            indent_print("  recipes:")

            if item == "Cut Copper":
                indent_print("  - output: 4")
                indent_print("    recipe_type: Crafting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Copper")+": -4")
                indent_print("  - output: 1")
                indent_print("    recipe_type: Cutting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Copper")+": -1")
            elif item == "Cut Copper Stairs":
                indent_print("  - output: 4")
                indent_print("    recipe_type: Crafting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Cut Copper")+": -6")
                indent_print("  - output: 1")
                indent_print("    recipe_type: Cutting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Copper")+": -1")
                indent_print("  - output: 1")
                indent_print("    recipe_type: Cutting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Cut Copper")+": -1")
            elif item == "Cut Copper Slab":
                indent_print("  - output: 6")
                indent_print("    recipe_type: Crafting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Cut Copper")+": -3")
                indent_print("  - output: 2")
                indent_print("    recipe_type: Cutting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Copper")+": -1")
                indent_print("  - output: 2")
                indent_print("    recipe_type: Cutting")
                indent_print("    requirements:")
                indent_print("      "+mrep(waxed + oxidization + "Cut Copper")+": -1")

            if waxed == "":
                for i in range(oxidization_level):
                    required_oxidization = oxidization_levels[i]
                    indent_print("  - output: 1")
                    indent_print("    recipe_type: Oxidization")
                    indent_print("    requirements:")
                    indent_print("      "+mrep(required_oxidization+item)+": -1")
            else:
                indent_print("  - output: 1")
                indent_print("    recipe_type: Crafting")
                indent_print("    requirements:")
                indent_print("      "+mrep(oxidization + item)+": -1")
                indent_print("      Honecomb: -1")

            indent_print("  - recipe_type: Raw Resource")
            print_chunk()

            # indent_print("")


# Block of Copper:
# Exposed Copper:
# Weathered Copper:
# Oxidized Copper:


# Cut Copper:
# Exposed Cut Copper:
# Weathered Cut Copper:
# Oxidized Cut Copper:
# Cut Copper Stairs:
# Exposed Cut Copper Stairs:
# Weathered Cut Copper Stairs:
# Oxidized Cut Copper Stairs:
# Cut Copper Slab:
# Exposed Cut Copper Slab:
# Weathered Cut Copper slab:
# Oxidized Cut Copper Slab:
# Waxed Block of Copper:
# Waxed Exposed Copper:
# Waxed Weathered Copper:
# Waxed Oxidized Copper:
# Waxed Cut Copper:
# Waxed Exposed Cut Copper:
# Waxed Weathered Cut Copper:
# Waxed Weathered Cut Copper:
# Waxed Oxidized Cut Copper:
# Waxed Cut Copper Stairs:
# Waxed Exposed Cut Copper Stairs:
# Waxed Weathered Cut Copper Stairs:
# Waxed Oxidized Cut Copper Stairs:
# Waxed Cut Copper Slab:
# Waxed Exposed Cut Copper Slab:
# Waxed Weathered Cut Copper slab:
# Waxed Oxidized Cut Copper Slab:



