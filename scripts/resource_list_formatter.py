################################################################################
# Simple script that loads and saves the yaml resource file to create
# consistent formatting across them
################################################################################
import argparse
import difflib
import os
import sys
import yaml
sys.path.append("../")
from pylib.resource_list import ResourceList  # noqa: E402
from pylib.yaml_token_load import ordered_load  # noqa: E402


################################################################################
# main
#
# The main function that handles argument parsing and calling the yaml format
# functions.
################################################################################
def main() -> None:
    parser = argparse.ArgumentParser(
        description='Format resources.yaml files'
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Formats all of the yaml files in the resource_lists directory"
    )
    parser.add_argument(
        "path",
        nargs='?',
        help="Formats only the file file specified"
    )
    parser.add_argument(
        "--inline",
        action="store_true",
        help="Write the formatted data back to the input file instead of a new file"
    )
    args = parser.parse_args()

    if args.all:
        for calculator in os.listdir("../resource_lists"):
            folder_path = os.path.join("../resource_lists", calculator)
            if not os.path.isdir(folder_path):
                continue
            resource_path = os.path.join(folder_path, "resources.yaml")
            print(resource_path)
            format_single_file(resource_path, same_file=True)

    elif args.path is not None:
        format_single_file(args.path, same_file=args.inline)

    else:
        parser.print_help()


################################################################################
# format_single_file
#
# Reads a single yaml file specified by input_filepath and outputs a formatted
# version of the file to a new file with the ".formatted" suffix. If same_file
# is set to True then the output is written in place to the input file instead.
################################################################################
def format_single_file(input_filepath: str, same_file: bool = False) -> None:
    if same_file:
        output_filepath = input_filepath
    else:
        output_filepath = input_filepath + ".formatted"

    errors = []
    with open(input_filepath, 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    if len(errors) > 0:
        print("There was an issue reading the file", input_filepath, errors)

    with open(output_filepath, 'w') as f:
        f.write("---\n")
        f.write(resource_list.to_yaml())
        f.write("\n")

    print(diff_yaml(input_filepath, output_filepath))


################################################################################
# diff_yaml
#
# A sanity check function used to confirm that the formatter did not change any
# of the actual data and just the formatting of it.
################################################################################
def diff_yaml(file_a_path: str, file_b_path: str) -> str:
    with open(file_a_path, 'r', encoding="utf_8") as f:
        data_a = yaml.dump(
            yaml.safe_load(f.read()),
            default_flow_style=False
        ).splitlines()
    with open(file_b_path, 'r', encoding="utf_8") as f:
        data_b = yaml.dump(
            yaml.safe_load(f.read()),
            default_flow_style=False
        ).splitlines()

    diff = difflib.unified_diff(
        data_a,
        data_b,
        fromfile=file_a_path,
        tofile=file_b_path
    )

    return "\n".join(diff)


if __name__ == "__main__":
    main()
