import argparse
import os
from typing import Dict, Tuple, List
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import queue

from pylib.calculator_producer import calculator_producers
from pylib.editor_producer import editor_producers
from pylib.gz_compressor_producer import gz_compressor_producers
from pylib.imagepack import item_image_producers
from pylib.landing_page_producer import landing_page_producers
from pylib.producer import Producer, Scheduler, SingleFile, GenericProducer, producer_copyfile, copy_file_with_hash
from pylib.producer_plugins import plugins_producers
from pylib.typescript_producer import typescript_producer
from pylib.uglifyjs import uglify_js_producer
from pylib.yaml_linter_producer import resource_list_parser_producers


# CLI Argument Flags
# FLAG_skip_js_lint = False
# FLAG_skip_index = False
# FLAG_skip_gz_compression = False
# FLAG_skip_image_compress = False
# FLAG_force_image = False
# FLAG_skip_plugins = False


################################################################################
# core_resource_producers
#
# Create the producers definitions for all of the core resources found in the
# `./core` folder. These are essentially static files that might go through
# a small amount of processing, such as minification or compilation, but are
# not dynamic as most of the other files are.
################################################################################
def core_resource_producers() -> List[GenericProducer]:

    hashed_copyfiles = [
        "core/calculator.css",
        "core/add_game.png",
    ]

    # Files that should be copied out of the "core" folder.
    copyfiles = [
        "core/logo.png",
        "core/.htaccess",
        "core/ads.txt",
        "core/favicon.ico",
    ]

    # Typescript Projects that should be compiled into javascript.
    ts_project_configs = [
        "core/src/tsconfig.json"
    ]

    # Javascript files that should be minified for production.
    uglify_js_files = [
        "cache/calculator.js",
        "core/yaml_export.js",
    ]

    core_producers: List[GenericProducer] = []

    # Add a producer for each file that will be copied over to output/.
    for copyfile in hashed_copyfiles:
        core_producers.append(
            copy_file_with_hash(
                input_file_pattern="^{}$".format(copyfile),
                output_file_template="output/{filename}-{filehash}{extension}",
                cache_file_template= "cache/{filename}{extension}.json",
                categories=["core"],
            )
        )

    # Add a producer for each file that will be copied over to output/.
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

    # Add a producer for each of the typescript project files.
    for ts_project_config in ts_project_configs:
        core_producers.append(typescript_producer(ts_project_config, ["core"]))

    # Add a producer for each javascript file to minify.
    for uglify_js_file in uglify_js_files:
        core_producers.append(
            uglify_js_producer(
                input_file=uglify_js_file,
                output_file=os.path.join("output", os.path.basename(uglify_js_file)),
                categories=["core"]
            )
        )

    return core_producers


################################################################################
# core_resource_paths
#
# The paths generator for all of the core resources that get copied over from
# the core/ folder to the output/ folder directly.
################################################################################
def core_resource_paths(input_files: SingleFile, groups: Dict[str, str]) -> Tuple[SingleFile, SingleFile]:
    return (
        input_files,
        {
            "file": os.path.join("output", os.path.basename(input_files["file"]))
        }
    )


################################################################################
# main
#
# The main process for the build.py script. Handles argument parsing and
# starting up the generator process.
################################################################################
def main() -> None:
    parser = argparse.ArgumentParser(
        description='Compile resourcecalculator.com html pages.'
    )

    parser.add_argument('limit_files', nargs='*', help="Speed up dev-builds by only building a specific set of one or more calculators")

    parser.add_argument('--watch', action='store_true', help="Watch source files and automatically rebuild when they change")
    # parser.add_argument('--draft', action='store_true', help="Enable all speed up flags for dev builds")

    # # parser.add_argument('--no-jslint', action='store_true', help="Speed up dev-builds by skipping linting javascript files")
    # parser.add_argument('--no-uglify-js', action='store_true', help="Speed up dev-builds by skipping javascript compression")
    # parser.add_argument('--no-gz', action='store_true', help="Speed up dev-builds by skipping gz text compression")
    # parser.add_argument('--no-index', action='store_true', help="Speed up dev-builds by skipping building the index page")
    # parser.add_argument('--no-image-compress', action='store_true', help="Speed up dev-builds by skipping the image compresson")
    # parser.add_argument('--no-plugins', action='store_true', help="Skip plugin publication to get only the plain calculators")

    # parser.add_argument('--force-html', action='store_true', help="Force the html pages to be rebuilt even if they are newer then their source files")
    # parser.add_argument('--force-image', action='store_true', help="Force images to be rebuilt even if they are newer then their source files")

    # global FLAG_skip_index
    # # global FLAG_skip_js_lint
    # global FLAG_skip_gz_compression
    # global FLAG_skip_image_compress
    # global FLAG_force_image
    # global FLAG_skip_plugins

    args = parser.parse_args()
    # if (args.watch):
    #     pass

    # # if args.no_jslint or args.draft:
    #     # FLAG_skip_js_lint = True

    # # if args.no_uglify_js or args.draft:
    # #     set_skip_uglify_flag()

    # if args.no_gz or args.draft:
    #     FLAG_skip_gz_compression = True

    # if args.no_image_compress or args.draft:
    #     FLAG_skip_image_compress = True

    # if args.no_index or args.draft:
    #     FLAG_skip_index = True

    # if args.force_image:
    #     FLAG_force_image = True

    # if args.no_plugins or args.draft:
    #     FLAG_skip_plugins = True

    # calculator_page_sublist = []


    calculator_dir_regex = r"[a-z ]+"
    if len(args.limit_files) >= 1:
        calculator_page_sublist = args.limit_files
        calculator_dir_regex = "|".join(calculator_page_sublist)

    producers: List[GenericProducer] = []
    producers += core_resource_producers()

    producers += resource_list_parser_producers(calculator_dir_regex)
    producers += item_image_producers(calculator_dir_regex)
    producers += calculator_producers(calculator_dir_regex)
    producers += editor_producers(calculator_dir_regex)
    producers += landing_page_producers(calculator_dir_regex)
    producers += plugins_producers(calculator_dir_regex)
    producers += gz_compressor_producers()


    scheduler = Scheduler(
        producer_list=producers,
        initial_filepaths=Scheduler.all_paths_in_dir(
            base_dir=".",
            ignore_paths=["venv_docker", "venv", ".git", "node_modules", "output_master"]
        )
    )


    watch_directory = "."

    if args.watch:
        q = queue.Queue()

        observer = Observer()

        event_handler = Handler(q)
        observer.schedule(event_handler, watch_directory, recursive = True)
        observer.start()
        try:
            while True:
                event_type, src_path = q.get(True)

                # TODO: Use .get_nowait after a successful "get" so we can bundle
                # anything in the queue together into a single operation to the
                # scheduler objects, instead of sending each file one by one.

                if event_type == 'created' or event_type == 'modified':
                    scheduler.add_or_update_files([src_path])
                elif event_type == 'deleted':
                    scheduler.delete_files([src_path])
                elif event_type == 'closed':
                    # A file was closed, does not seem as useful as modified
                    pass
                else:
                    print("Unknown Event", event_type)

        except:
            observer.stop()
            print("Observer Stopped")

        observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, event_queue: queue.Queue):
        self.event_queue = event_queue
    def on_any_event(self, event):

        if event.is_directory:
            return

        self.event_queue.put((event.event_type, event.src_path[2:]))




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
