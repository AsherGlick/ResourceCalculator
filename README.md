ResourceCalculator.com is a website that can calculate required resources from a list of final requirements, and tell you how to get from the raw resources to the final resources.

![Resource Calculation Screenshot](screenshot01.png "Resource Calculation Screenshot")


Creating or Updating a Calculator
=================================
If you want to add a new resource list to the calculator, you will only need 4 things:  
1. A folder in `resource_lists/` for all the files to live in (eg: [resource_lists/minecraft](resource_lists/minecraft))
2. A **460px** by **215px** thumbnail of the game you are making a calculator for (eg: [resource_lists/minecraft/icon.jpg](resource_lists/minecraft/icon.jpg))
    * These are the same dimensions as the thumbnail in the Steam store.
3. A set of rectangular images of uniform size for each of the resources (eg: [resource_lists/minecraft/items/](resource_lists/minecraft/items/))
4. The list of resources and what is needed to obtain them (eg: [resource_lists/minecraft/resources.yaml](resource_lists/minecraft/resources.yaml))

resources.yaml
--------------
The resource list is a yaml file that contains all the recipes for each item in the game. All items will have a "Raw Resource" type to allow users to ignore any materials needed for crafting that resource, and because some resources are base resources that you cannot craft.
Though key/value mappings are not inherently ordered, when we build the calculator page, their order is preserved from the yaml file
allowing one to order the items coherently.
```
resources:
  Lithium:
    recipes:
      - recipe_type: Raw Resource

  Small Battery:
    recipes:
    - output: 1
      recipe_type: Backpack Printer
      requirements:
        Lithium: -1
    - recipe_type: Raw Resource

  Medium Battery:
    recipes:
    - output: 1
      recipe_type: Printer
      requirements:
        Lithium: -2
    - recipe_type: Raw Resource
```
For ease of reading we will always have the key order be `output`, `recipe_type`, `requirements`, and then optionally `extra_data` where you can store extra information about the item in an unstructured map

items/[itemname].png
-----------
For each item in your resources.yaml file you will need to have an image for that resource. If an image is missing, then the build process will submit a warning and fill that space with a purple color, indicating it does not have an icon.
The icons can be any size, even rectangular, but they all must be the same size as each other for a given calculator.
The file names of each file should be the resource name in all lower case with no spaces or punctuation.  

For Example:  
*"Pink Stained Glass Pane"* becomes *[pinkstainedglasspane.png](resource_lists/minecraft/items/pinkstainedglasspane.png)*  
*"Jack 'o Lantern"* becomes *[jackolantern.png](resource_lists/minecraft/items/jackolantern.png)*

icon.jpg
--------
The icon needs to be `460px` by `215px` to fit in with the other calculator links. It also needs to be a `jpg`, not a `png` or other image file.

The Steam page for a game uses a `jpg` thumbnail with those dimensions, so simple downloading it to the appropriate directory and renaming to `icon.jpg` should be all that is needed.

Compiling The Calculator
========================

On linux, you will need to have python3 installed as well as several python dependencies found in requirements.txt
```
sudo apt install python3 python3-pip pngquant npm
pip3 install -r requirements.txt
npm install
python3 build.py
```
On windows you should be able to install the same dependencies via pip and npm though I am unsure how to use pngquant on windows, `build.py` should work without being able to run the png compression however.

You can also run the calculator locally in Docker by running:

```
docker build . -t resourcecalculator
docker run -dit --name resourcecalculator -p 8080:80 resourcecalculator
```

This creates a local docker container that compiles the current working directory, starts the container and exposes it locally at `127.0.0.1:8080`. To test changes, stop and delete the container and re-run the two commands.
