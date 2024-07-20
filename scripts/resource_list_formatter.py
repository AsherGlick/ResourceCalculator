################################################################################
# Simple script that loads and saves the yaml resource file to create
# consistent formatting across them
################################################################################
import sys
sys.path.append("../")
from pylib.resource_list import ResourceList
import yaml
from pylib.yaml_token_load import ordered_load
import yaml
import difflib


def main():
    input_filepath = sys.argv[1]
    output_filepath = sys.argv[1] + ".formatted"
    errors = []
    with open(input_filepath, 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    print(errors)

    with open(output_filepath, 'w') as f:
        f.write("---\n")
        f.write(resource_list.to_yaml())
        f.write("\n")

    print(diff_yaml(input_filepath, output_filepath))


def diff_yaml(file_a_path: str, file_b_path: str):
    with open(file_a_path, 'r', encoding="utf_8") as f:
        data_a = yaml.dump(yaml.safe_load(f.read()), default_flow_style=False).splitlines()
    with open(file_b_path, 'r', encoding="utf_8") as f:
        data_b = yaml.dump(yaml.safe_load(f.read()), default_flow_style=False).splitlines()

    diff = difflib.unified_diff(data_a, data_b, fromfile=file_a_path, tofile=file_b_path)
    
    return "\n".join(diff)


if __name__ == "__main__":
    main()
