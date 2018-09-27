import json
import re
import os
from jinja2 import Environment, FileSystemLoader
import yaml
from shutil import copyfile
import math
from collections import OrderedDict
from PIL import Image

import subprocess

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
    output_image_path = os.path.join(calculator_folder, resource_list+".png")
    result.save(output_image_path)

    # # pngquant and optipng both seemed to compress the image further. Optipng only doing slightly more <.5% on average after receiving the pngquant image
    # # convert however tended to tripple the size of the file, still under the original filesize but a terrible step in the pipeline
    # size_0 = os.path.getsize(output_image_path)
    # print(size_0)
    subprocess.run(["pngquant", "--force", "--ext", ".png", "256", "--nofs", output_image_path])
    # size_1 = os.path.getsize(output_image_path)
    # subprocess.run(["convert", "-verbose", "-strip", output_image_path, output_image_path])
    # size_2 = os.path.getsize(output_image_path)
    # subprocess.run(["optipng", "-o7", output_image_path])
    # size_3 = os.path.getsize(output_image_path)

    # import time
    # print("pngquaint", size_1, "(" + str(round(((size_1/size_0))*100, 1)) + "% of original)")
    # time.sleep(1)
    # print("imgmagick convert", size_2, "(" + str(round(((size_2/size_1))*100, 1)) + "% of last)", "(" + str(round(((size_2/size_0))*100, 1)) + "% of original)")
    # time.sleep(1)
    # print("optipng", size_3, "(" + str(round(((size_3/size_2))*100, 1)) + "% of last)", "(" + str(round(((size_3/size_0))*100, 1)) + "% of original)")
    # system("pngquant --force --ext .png 256 --nofs app/assets/images/items/#{name}.png")
    # system("convert -verbose -strip app/assets/images/items/#{name}.png app/assets/images/items/#{name}.png") # remove the sRGB data that pngquaint adds in versions < 2.6
    # system("optipng -o7 app/assets/images/items/#{name}.png")



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

    raw_resource_count = 0
    for recipe in recipes:

        if (recipe['recipe_type'] == "Raw Resource"):
            if (recipe == OrderedDict([('output', 1), ('recipe_type', 'Raw Resource'), ('requirements', OrderedDict([(item_name, 0)]))])):
                raw_resource_count += 1
            else:
                print(resource_list.upper()+":", item_name, "has an invalid \"Raw Resource\"")

    if raw_resource_count == 0:
        print(resource_list.upper()+":", item_name, "must have a \"Raw Resource\" which outputs 1 and has a requirement of 0 of itself")
    elif raw_resource_count > 1:
        print(resource_list.upper()+":", item_name, "must have only one \"Raw Resource\"")


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
        # item_styles[simple_name] = "width: "+str(image_width)+"px; height: "+str(image_height)+"px; background: #8a8a8a url("+resource_list+".png) 0 0 no-repeat;"
        # item_styles[simple_name] = ""

        if simple_name in resource_image_coordinates:
            x_coordinate, y_coordinate = resource_image_coordinates[simple_name]
            # item_styles[simple_name] += "background: #8a8a8a url("+resource_list+".png) "+str(-x_coordinate)+"px "+str(-y_coordinate)+"px no-repeat;"
            item_styles[simple_name] = "background-position: "+str(-x_coordinate)+"px "+str(-y_coordinate)+"px;"
        else:
            item_styles[simple_name] = "background: #f0f; background-image: none;"
            print("WARNING:", simple_name, "has a recipe but no image and will appear purple in the calculator")

        resource["mc_value"] = recipe
        resource["simplename"] = simple_name
        resources.append(resource)

    output_from_parsed_template = template.render(resources=resources, recipe_json=recipe_json, item_width=image_width, item_height=image_height, item_styles=item_styles, resource_list=resource_list, authors=authors)

    with open(os.path.join(calculator_folder, "index.html"), "w") as f:
        f.write(output_from_parsed_template)

    # Sanity Check Warning, is there an image that does not have a recipe
    simple_resources = [x["simplename"] for x in resources]
    for simple_name in resource_image_coordinates:
        if simple_name not in simple_resources:
            print("WARNING:", simple_name, "has an image but no recipe and will not appear in the calculator")


def create_index(directories):
    for directory in directories:
        copyfile("resource_lists/" + directory + "/icon.png", "output/"+directory+"/icon.png")
        pass

    # Configure and begin the jinja2 template parsing
    env = Environment(loader=FileSystemLoader('core'))
    template = env.get_template("index.html")

    output_from_parsed_template = template.render(calculators=directories)

    with open(os.path.join("output", "index.html"), "w") as f:
        f.write(output_from_parsed_template)

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
    copyfile("core/logo.png", "output/logo.png")
    copyfile("core/.htaccess", "output/.htaccess")
    copyfile("core/add_game.png", "output/add_game.png")


def main():
    if not os.path.exists("output"):
        os.makedirs("output")
    # Create the calculators
    d = './resource_lists'
    calculator_directories = []
    for o in os.listdir(d):
        if os.path.isdir(os.path.join(d, o)):
            create_calculator(o)
            calculator_directories.append(o)

    calculator_directories.sort()
    create_index(calculator_directories)
    copy_common_resources()


main()
