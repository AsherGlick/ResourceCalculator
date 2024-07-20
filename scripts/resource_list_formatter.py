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
from pylib.resource_list import ResourceList
from pylib.yaml_token_load import ordered_load


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Format resources.yaml files'
    )
    parser.add_argument("--all", action="store_true", help="Formats all of the yaml files in the resource_lists directory")
    parser.add_argument("path", nargs='?', help="Formats a single file")
    parser.add_argument("--inline", action="store_true", help="Formats a file and writes it to the file")
    args = parser.parse_args()

    if args.all:
        for calculator in os.listdir("../resource_lists"):
            path = os.path.join("../resource_lists", calculator, "resources.yaml")
            print(path)
            format_single_file(path, same_file=True)

    elif args.path is not None:
        format_single_file(args.path, args.inline)


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


def diff_yaml(file_a_path: str, file_b_path: str) -> str:
    with open(file_a_path, 'r', encoding="utf_8") as f:
        data_a = yaml.dump(yaml.safe_load(f.read()), default_flow_style=False).splitlines()
    with open(file_b_path, 'r', encoding="utf_8") as f:
        data_b = yaml.dump(yaml.safe_load(f.read()), default_flow_style=False).splitlines()

    diff = difflib.unified_diff(data_a, data_b, fromfile=file_a_path, tofile=file_b_path)

    return "\n".join(diff)


if __name__ == "__main__":
    main()
