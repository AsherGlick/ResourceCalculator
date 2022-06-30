import argparse
import os
import re
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import OrderedDict, Union, TypedDict, TypeVar
from jinja2 import Environment, FileSystemLoader
from typing import Dict, Tuple, List, Any, TypedDict
from pylib.uglifyjs import uglify_js_producer
from pylib.resource_list import ResourceList, Resource, TokenError
from pylib.yaml_token_load import ordered_load
from pylib.producer import Producer, Scheduler, SingleFile
from pylib.typescript_producer import typescript_producer
from pylib.imagepack import item_image_producers
from pylib.calculator_producer import calculator_producers
from pylib.editor_producer import editor_producers
from pylib.yaml_linter_producer import resource_list_parser_producers
from pylib.gz_compressor_producer import gz_compressor_producers

from pylib.landing_page_producer import landing_page_producers
from pylib.producer_plugins import plugins_producers

# CLI Argument Flags
# FLAG_skip_js_lint = False
FLAG_skip_index = False
FLAG_skip_gz_compression = False
FLAG_skip_image_compress = False
FLAG_force_image = False
FLAG_skip_plugins = False


################################################################################
# A simple caching layer for loading and parsing resource lists. This is used
# in normal runs in order to rebuild the index page without re-parsing the
# entire yaml file for each calculator. It is also useful for --watch when not
# editing a resource list.
################################################################################
@dataclass
class CachedResourceList():
    resource_list: ResourceList
    timestamp: float
    errors: List[TokenError]


resource_list_cache: Dict[str, CachedResourceList] = {}


def load_resource_list(filepath: str) -> Tuple[ResourceList, List[TokenError]]:
    global resource_list_cache
    last_modified_time = os.path.getctime(filepath)

    if (filepath not in resource_list_cache or resource_list_cache[filepath].timestamp > last_modified_time):
        errors: List[TokenError] = []

        with open(filepath, 'r', encoding="utf_8") as f:
            yaml_data = ordered_load(f)
            resource_list = ResourceList()
            errors += resource_list.parse(yaml_data)

        resource_list_cache[filepath] = CachedResourceList(
            resource_list=resource_list,
            timestamp=last_modified_time,
            errors=errors
        )
    else:
        print("  Using Cached", filepath)

    return (resource_list_cache[filepath].resource_list, resource_list_cache[filepath].errors)




################################################################################
# lint_javascript
#
# This function will attempt to call a javascript linter on the calculator.js
# file. If the linting process fails then a warning will be thrown but the
# process will not be ended.
################################################################################
def lint_javascript() -> None:
    try:
        subprocess.run(["./node_modules/.bin/eslint", "core/calculator.js"])
    except OSError as e:
        print("WARNING: Javascript linting failed")
        print("        ", e)




################################################################################
# get_oldest_modified_time
#
# This function takes a directory and finds the oldest modification time of any
# file in that directory.
################################################################################
def get_oldest_modified_time(path: str) -> float:
    time_list = []
    for file in os.listdir(path):
        filepath = os.path.join(path, file)
        if (os.path.isdir(filepath)):
            time_list.append(get_oldest_modified_time(filepath))
        else:
            time_list.append(os.path.getctime(filepath))
    if len(time_list) == 0:
        return 0
    return min(time_list)


################################################################################
# get_newest_modified_time
#
# This function takes in a directory and finds the newest modification time of
# any file in that directory
################################################################################
def get_newest_modified_time(path: str, ignore: List[str] = []) -> float:
    time_list = [os.path.getctime(path)]
    for file in os.listdir(path):
        if file in ignore:
            continue

        filepath = os.path.join(path, file)
        if (os.path.isdir(filepath)):
            time_list.append(get_newest_modified_time(filepath))
        else:
            time_list.append(os.path.getctime(filepath))
    return max(time_list)


def touch_output_folder_files(calculator_folder: str, timestamp: int = 0) -> None:
    if timestamp == 0:
        timestamp = int(time.time())

    for file in os.listdir(calculator_folder):
        filepath = os.path.join(calculator_folder, file)
        if (os.path.isdir(filepath)):
            touch_output_folder_files(filepath, timestamp)
        else:
            os.utime(filepath, (timestamp, timestamp))


def publish_calculator_plugins(
    calculator_folder: str,
    source_folder: str
) -> None:
    plugin_output_folder = os.path.join(calculator_folder, "plugins")
    plugin_source_folder = os.path.join(source_folder, "plugins")

    if os.path.exists(plugin_source_folder) and not FLAG_skip_plugins:
        should_publish_plugins = True

        if os.path.exists(plugin_output_folder):
            newest_file = max(
                os.path.getctime("build.py"),  # Check generator code modification
                get_newest_modified_time(plugin_source_folder),  # Check source plugin modification
            )
            should_publish_plugins = newest_file > os.path.getctime(plugin_output_folder)

        if should_publish_plugins:
            shutil.copytree(plugin_source_folder, plugin_output_folder, dirs_exist_ok=True)



################################################################################
# create_index_page
#
# This function creates an index page with all of the calculator links
################################################################################
def create_index_page(directories: List[str]) -> None:
    for directory in directories:
        shutil.copyfile("resource_lists/" + directory + "/icon.png", "output/" + directory + "/icon.png")

    # Configure and begin the jinja2 template parsing
    env = Environment(loader=FileSystemLoader('core'))
    template = env.get_template("index.html")

    calculators = []
    for directory in directories:
        calculator_data = {
            "path": directory,
            "display_name": calculator_display_name(directory)
        }

        calculators.append(calculator_data)

    output_from_parsed_template = template.render(calculators=calculators)

    with open(os.path.join("output", "index.html"), "w", encoding="utf_8") as f:
        f.write(output_from_parsed_template)


################################################################################
# calculator_display_name
#
# Reads the resources yaml file and grabs the display name of that calculator
#
# TODO: This function is very slow because it parses the entire yaml file again
#       maybe there can be some caching that happens here.
################################################################################
def calculator_display_name(calculator_name: str) -> str:
    resource_list_file = os.path.join("resource_lists", calculator_name, "resources.yaml")
    resource_list, parse_errors = load_resource_list(resource_list_file)
    return resource_list.index_page_display_name


################################################################################
# core_resource_producers
#
# Create the producers definitions for all of the core resources found in the
# `./core` folder.
################################################################################
def core_resource_producers() -> List[Producer]:
    # Files that should be copied out of the "core" folder
    copyfiles = [
        "core/calculator.css",
        "core/logo.png",
        "core/.htaccess",
        "core/add_game.png",
        "core/ads.txt",
        "core/favicon.ico",
    ]

    ts_project_configs = [
        "core/src/tsconfig.json"
    ]

    # JS files to be minified
    uglify_js_files = [
        "cache/calculator.js",
        "core/yaml_export.js",
    ]

    core_producers: List[Producer] = []

    for copyfile in copyfiles:
        core_producers.append(
            Producer(
                input_path_patterns={
                    "file": "^{}$".format(copyfile),
                },
                paths=core_resource_paths,
                function=producer_copyfile,
                categories=["core"]
            )
        )

    # Add the core typescript file
    for ts_project_config in ts_project_configs:
        core_producers += typescript_producer(ts_project_config, ["core"])

    for uglify_js_file in uglify_js_files:
        core_producers.append(
            uglify_js_producer(
                input_file=uglify_js_file,
                output_file=os.path.join("output", os.path.basename(uglify_js_file)),
                categories=["core"]
            )
        )

    return core_producers


def core_resource_paths(input_files: SingleFile, groups: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    return (
        input_files,
        {
            "file": os.path.join("output", os.path.basename(input_files["file"]))
        }
    )
    
def producer_copyfile(input_files: SingleFile, output_files: SingleFile) -> None:
    input_file: str = input_files["file"]
    output_file: str = output_files["file"]

    # Copy the file
    shutil.copyfile(input_file, output_file)



def main() -> None:
    parser = argparse.ArgumentParser(
        description='Compile resourcecalculator.com html pages.'
    )

    parser.add_argument('limit_files', nargs='*', help="Speed up dev-builds by only building a specific set of one or more calculators")

    parser.add_argument('--watch', action='store_true', help="Watch source files and automatically rebuild when they change")
    parser.add_argument('--draft', action='store_true', help="Enable all speed up flags for dev builds")

    # parser.add_argument('--no-jslint', action='store_true', help="Speed up dev-builds by skipping linting javascript files")
    parser.add_argument('--no-uglify-js', action='store_true', help="Speed up dev-builds by skipping javascript compression")
    parser.add_argument('--no-gz', action='store_true', help="Speed up dev-builds by skipping gz text compression")
    parser.add_argument('--no-index', action='store_true', help="Speed up dev-builds by skipping building the index page")
    parser.add_argument('--no-image-compress', action='store_true', help="Speed up dev-builds by skipping the image compresson")
    parser.add_argument('--no-plugins', action='store_true', help="Skip plugin publication to get only the plain calculators")

    parser.add_argument('--force-html', action='store_true', help="Force the html pages to be rebuilt even if they are newer then their source files")
    parser.add_argument('--force-image', action='store_true', help="Force images to be rebuilt even if they are newer then their source files")

    global FLAG_skip_index
    # global FLAG_skip_js_lint
    global FLAG_skip_gz_compression
    global FLAG_skip_image_compress
    global FLAG_force_image
    global FLAG_skip_plugins

    args = parser.parse_args()
    if (args.watch):
        pass

    # if args.no_jslint or args.draft:
        # FLAG_skip_js_lint = True

    # if args.no_uglify_js or args.draft:
    #     set_skip_uglify_flag()

    if args.no_gz or args.draft:
        FLAG_skip_gz_compression = True

    if args.no_image_compress or args.draft:
        FLAG_skip_image_compress = True

    if args.no_index or args.draft:
        FLAG_skip_index = True

    if args.force_image:
        FLAG_force_image = True

    if args.no_plugins or args.draft:
        FLAG_skip_plugins = True

    calculator_page_sublist = []
    if len(args.limit_files) >= 1:
        FLAG_skip_index = True
        calculator_page_sublist = args.limit_files
        print("Only building", ", ".join(calculator_page_sublist))

    # if not FLAG_skip_js_lint:
    #     lint_javascript()

    # if not os.path.exists("output"):
    #     os.makedirs("output")


    producers: List[Producer] = []

    producers += resource_list_parser_producers()
    producers += item_image_producers()
    producers += calculator_producers()
    producers += editor_producers()
    producers += core_resource_producers()
    producers += landing_page_producers()
    producers += plugins_producers()
    producers += gz_compressor_producers()


    studio = Scheduler(producers,  Scheduler.all_paths_in_dir(".", ["venv_docker", "venv", ".git", "node_modules", "output_master"]))

    # build_producer_calls(producers, ["venv_docker", "venv", ".git", "node_modules"])

    # if args.watch:
    #     # If the watch argument is given then poll for changes of the files
    #     # polling is used instead of something like inotify because change
    #     # events are not propagated for volumes being run on docker for
    #     # windows. If ever a nicer solution for handling this appears this
    #     # code can be changed to support it.
    #     #
    #     # NOTE: With this polling method there is a race condition that is
    #     # possible to hit rather if saving frequently. If a file is
    #     # updated during its generation, after it has been read but before
    #     # the first file is written then it will not be detected in the
    #     # next pass-through.
    #     time.sleep(.5)
    #     continue
    # else:
    #     break

# @dataclass
# class ADataclassType:
#     input_file: str
#     input_files: List[str]

# class ATypedDictClass(TypedDict):
#     input_file: str
#     input_files: List[str]

# class AnotherTYpedDictClass(TypedDict):
#     output_file: str
#     output_files: List[str]

# def main2():
#     print("hello world")

#     a_dataclass_type:ADataclassType = ADataclassType(input_file="file", input_files=["file1", "file2"])
#     a_typeddict_type:ATypedDictClass = ATypedDictClass(input_file="file", input_files=["file1", "file2"])


#     print(a_dataclass_type)
#     # print(a_dataclass_type["input_file"])

#     print(a_typeddict_type)
#     astr: str = a_typeddict_type["input_file"]
#     print(astr)

#     afunction(a_typeddict_type)


# T = TypeVar("T", bound=TypedDict)

# def afunction (argone: T) -> T:
#     print(isinstance(argone, dict))
#     print(argone)

#     output_files = AnotherTYpedDictClass(output_file="f", output_files=["a", "b"])

#     return output_files


PROFILE = False
if __name__ == "__main__":

    if PROFILE:
        import cProfile
        import pstats

        with cProfile.Profile() as pr:
            main()

        stats = pstats.Stats(pr)
        stats.sort_stats(pstats.SortKey.TIME)
        stats.dump_stats(filename="profiledata.prof")
        # Useful to use snakeviz to display profile data `snakeviz profiledata.prof`
    else:
        main()
