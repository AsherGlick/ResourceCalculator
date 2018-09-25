import json
import re
import os
from jinja2 import Environment, FileSystemLoader
import yaml
from shutil import copyfile
import math
from collections import OrderedDict
from PIL import Image

################################################################################
# ordered_load
#
# This function will load in the yaml recipe file but maintain the order of the
# items. This allows us to simplify the file definition making it easier for
# humans to use while also allowing us to set the order of the items for easy
# grouping
################################################################################
# https://stackoverflow.com/questions/5121931/in-python-how-can-you-load-yaml-mappings-as-ordereddicts
def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)


################################################################################
# create_packed_image
#
# This function will take all the files within the resource_lists/[list]/items
# and create a single packed image of them. Then return the coordinates so that
# css can be written to load all of the images from the same file instead of
# making a large number of get requests for the file
################################################################################
def create_packed_image(resource_list):

    resource_image_folder = os.path.join("resource_lists", resource_list, "items")

    image_coordinates = {}

    standard_width = None
    standard_height = None

    images = []
    # resources = []

    for file in os.listdir(resource_image_folder):
        image = Image.open(os.path.join(resource_image_folder, file))
        images.append((os.path.os.path.splitext(file)[0], image))
        width, height = image.size
        # Validate that all images are the same size
        if (standard_width is None and standard_height is None):
            standard_height = height
            standard_width = width
        elif (standard_width != width or standard_height != height):
            print("ERROR: All resource list item images must be the same size")

    # Sort the images, this is probably not nessasary but will allow for
    # differences between files to be noticed with less noise of random shifting of squares
    images.sort(key=lambda x: x[0])

    # Use our special math function to determine what the number of columns
    # should be for the final packed image.
    # Programmers note: This was a lot of fun to figure out and derrived strangely
    columns = math.ceil(math.sqrt(standard_height * len(images) / standard_width))
    result_width = standard_width*columns
    result_height = standard_height*math.ceil((len(images)/columns))

    # Create a new output file and write all the images to spots in the file
    result = Image.new('RGBA', (result_width, result_height))
    for index, (name, image) in enumerate(images):
        x_coordinate = (index % columns)*standard_height
        y_coordinate = math.floor(index/columns)*standard_width
        image_coordinates[name] = (x_coordinate, y_coordinate)
        result.paste(im=image, box=(x_coordinate, y_coordinate))

    # save the new packed image file and all the coordinates of the images
    calculator_folder = os.path.join("output", resource_list)
    result.save(os.path.join(calculator_folder, resource_list+".png"))

    # TODO: Compress the image after it has been exported, or before if possible

    return (standard_width, standard_height, image_coordinates)



def lint_recipe(resource_list, item_name, recipes):

    required_keys = ["output", "recipe_type", "requirements"]
    optional_keys = ["extra_data"]

    valid_keys = required_keys + optional_keys

    for i, recipe in enumerate(recipes):

        recipe_keys = [x for x in recipe]

        # Make sure all the required keys exist
        for required_key in required_keys:
            if required_key not in recipe_keys:
                print(resource_list.upper()+":", "\""+required_key+"\" is not in", item_name, "recipe", i)

        # Make sure that all the keys being used are valid keys
        for recipe_key in recipe_keys:
            if recipe_key not in valid_keys:
                print(resource_list.upper()+":", "\""+recipe_key+"\" in", item_name, "recipe", i, "is not a valid key")

        # Validate the keys are in the right order to promote uniformity in the templates
        if (recipe_keys[0] != valid_keys[0]):
            # print(item_name, "recipe", i, "should have the first element of the hash be \"output\"")
            print(resource_list.upper()+":", "\"output\" should be the first key of", item_name, "recipe", i)
        if (recipe_keys[1] != valid_keys[1]):
            # print(item_name, "recipe", i, "should have the first element of the hash be \"output\"")
            print(resource_list.upper()+":", "\"recipe_type\" should be the second key of", item_name, "recipe", i)
        if (recipe_keys[2] != valid_keys[2]):
            # print(item_name, "recipe", i, "should have the first element of the hash be \"output\"")
            print(resource_list.upper()+":", "\"requirements\" should be the third key of", item_name, "recipe", i)


def create_calculator(resource_list):
    calculator_folder = os.path.join("output", resource_list)
    if not os.path.exists(calculator_folder):
        os.makedirs(calculator_folder)
    print(calculator_folder)

    # Create a packed image of all the item images
    image_width, image_height, resource_image_coordinates = create_packed_image(resource_list)

    # Configure and begin the jinja2 template parsing
    env = Environment(loader=FileSystemLoader('core'))
    template = env.get_template("calculator.html")

    # Load in the yaml resources file
    with open(os.path.join("resource_lists", resource_list, "resources.yaml")) as f:
        yaml_data = ordered_load(f, yaml.SafeLoader)
    recipes = yaml_data["resources"]
    authors = yaml_data["authors"]

    # run some sanity checks on the recipes
    for recipe in recipes:
        lint_recipe(resource_list, recipe, recipes[recipe])

    recipe_json = json.dumps(recipes)

    resources = []
    item_styles = {}
    for recipe in recipes:
        resource = {}
        simple_name = re.sub(r'[^a-z]', '', recipe.lower())
        item_styles[simple_name] = "width: "+str(image_width)+"px; height: "+str(image_height)+"px; "

        if simple_name in resource_image_coordinates:
            x_coordinate, y_coordinate = resource_image_coordinates[simple_name]
            item_styles[simple_name] += "background: url("+resource_list+".png) "+str(-x_coordinate)+"px "+str(-y_coordinate)+"px no-repeat;"
        else:
            item_styles[simple_name] += "background: #f0f;"
            print("WARNING:", simple_name, "has a recipe but no image and will appear purple in the calculator")

        resource["mc_value"] = recipe
        resource["simplename"] = simple_name
        resources.append(resource)

    output_from_parsed_template = template.render(resources=resources, recipe_json=recipe_json, item_width=image_width, item_height=image_height, item_styles=item_styles)


    with open(os.path.join(calculator_folder, "index.html"), "w") as f:
        f.write(output_from_parsed_template)

    # Sanity Check Warning, is there an image that does not have a recipe
    simple_resources = [x["simplename"] for x in resources]
    for simple_name in resource_image_coordinates:
        if simple_name not in simple_resources:
            print("WARNING:", simple_name, "has an image but no recipe and will not appear in the calculator")


################################################################################
# copy_common_resources
#
# This is a hacky function to copy over some files that should be accessable
# by the code
################################################################################
def copy_common_resources():
    copyfile("core/calculator.css", "output/calculator.css")
    copyfile("core/calculator.js", "output/calculator.js")
    copyfile("core/thirdparty/jquery-3.3.1.min.js", "output/jquery.js")
    copyfile("core/thirdparty/d3.v4.min.js", "output/d3.js")
    copyfile("core/thirdparty/sankey.js", "output/sankey.js")


def main():
    if not os.path.exists("output"):
        os.makedirs("output")
    # Create the calculators
    create_calculator("astroneer")
    create_calculator("minecraft")
    copy_common_resources()

main()