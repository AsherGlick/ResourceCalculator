import htmlmin  # type: ignore
from pylib.producer import Producer, SingleFile, GenericProducer
from typing import List, Tuple, OrderedDict, Dict, Any, TypedDict
import re
import os
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, get_primitive
from jinja2 import Environment, FileSystemLoader
import json
from pylib.uglifyjs import uglify_js_string
from pylib.json_data_compressor import mini_js_data
from pylib.webminify import minify_css_blocks
import pickle



def editor_producers() -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                "resources_pickle": r"^cache/(?P<calculator_dir>[a-z ]+)/resources\.pickle$",
                "image_layout_json": r"^cache/(?P<calculator_dir>[a-z ]+)/packed_image_layout\.json$",
                "editor_template": r"^core/edit\.html$",
            },
            paths=editor_paths,
            function=editor_function,
            categories=["editor"]
        )
    ]

class EditorInputFiles(TypedDict):
    resources_pickle: str
    image_layout_json: str
    editor_template: str


def editor_paths(input_files: EditorInputFiles, categories: Dict[str,str]) -> Tuple[EditorInputFiles, SingleFile]:
    calculator_page = categories["calculator_dir"]

    calculator_index_page = os.path.join("output", calculator_page, "edit.html")

    return (
        input_files,
        {
            "file": calculator_index_page,
        }
    )


def editor_function(input_files: EditorInputFiles, output_files: SingleFile) -> None:
    # calculator_name: str = match.group(1)
    # resource_list_file = os.path.join("cache", calculator_name, "resources.pickle")
    # image_metadata_file = os.path.join("cache", calculator_name, "packed_image_layout.json")
    
    resource_list_file = input_files["resources_pickle"]
    # input_files = [resource_list_file]

    # # if input_file not in input_files:
    # #     raise ValueError("Expected the input file to be one of:" + str(input_files) + " but got" + input_file)

    # if len(output_files) != 1:
    #     raise ValueError("Expected just one output file but got" + str(output_files))
    
    calculator_editor_html_filepath = output_files["file"]

    # Load and validate the type of the resource list data
    with open(resource_list_file, 'rb') as f:
        resource_list = pickle.load(f)
        if not isinstance(resource_list, ResourceList):
            raise ValueError("Pickled Resource List File is not a valid ResourceList class")

    env = Environment(loader=FileSystemLoader('core'))

    resource_list_js_data = mini_js_data(hack_update_version(get_primitive(resource_list)), "resource_list_json")

    editor_template = env.get_template("edit.html")

    rendered_editor = editor_template.render(
        resource_list_json=resource_list_js_data,
        element_height=55,  # should be automatically generated from the image height? width? or should be static
        total_height=55 * 989,  # Should be implemented in-javascript
        buffer_element_count=2,
    )

    minified_editor = rendered_editor
    # minified_editor = htmlmin.minify(rendered_editor, remove_comments=True, remove_empty_space=True)
    # minified_editor = minify_css_blocks(minified_editor)

    with open(calculator_editor_html_filepath, "w", encoding="utf_8") as f:
        f.write(minified_editor)


################################################################################
# hack_update_version
#
# Temporary file to update the resource file to the new format that does not
# use ordered dictionaries and instead uses arrays of dictionaries.
################################################################################
def hack_update_version(data: Any) -> Any:
    new_authors = []
    for author in data["authors"]:
        new_authors.append({
            "name":author,
            "link":data["authors"][author]
        })
    data["authors"] = new_authors

    new_resources = []
    resource_id_count = 1
    for resource in data["resources"]:
        new_resource = {
            "name": resource,
            "id": resource_id_count,
        }

        for key in data["resources"][resource]:
            new_resource[key] = data["resources"][resource][key]

        new_resources.append(new_resource)
        resource_id_count += 1
    data["resources"] = new_resources

    return data