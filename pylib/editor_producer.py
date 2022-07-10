from jinja2 import Environment, FileSystemLoader
from typing import List, Tuple, Dict, Any, TypedDict
import os
import pickle

from pylib.json_data_compressor import mini_js_data
from pylib.producer import Producer, SingleFile, GenericProducer
from pylib.resource_list import ResourceList, get_primitive


################################################################################
# editor_producers
#
# Creates a producer for the editor page that allows the user to edit a
# calculator via a graphical tool instead of via yaml or json.
################################################################################
def editor_producers(calculator_dir_regex: str) -> List[GenericProducer]:
    return [
        Producer(
            input_path_patterns={
                "resources_pickle": r"^cache/(?P<calculator_dir>{calculator_dir_regex})/resources\.pickle$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
                "image_layout_json": r"^cache/(?P<calculator_dir>{calculator_dir_regex})/packed_image_layout\.json$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
                "editor_template": r"^core/edit\.html$",
            },
            paths=editor_paths,
            function=editor_function,
            categories=["editor"]
        )
    ]


################################################################################
# EditorInputFiles
#
# A TypedDict representing the input files structure for the producers that
# create the editor pages.
################################################################################
class EditorInputFiles(TypedDict):
    resources_pickle: str
    image_layout_json: str
    editor_template: str


################################################################################
# editor_paths
#
# The input output path generation function for the editor producer.
################################################################################
def editor_paths(input_files: EditorInputFiles, categories: Dict[str, str]) -> Tuple[EditorInputFiles, SingleFile]:
    calculator_page = categories["calculator_dir"]

    calculator_index_page = os.path.join("output", calculator_page, "edit.html")

    return (
        input_files,
        {
            "file": calculator_index_page,
        }
    )


################################################################################
# editor_function
#
# The processing function that generates the output editor file given a struct
# of input and output files via the producer.
################################################################################
def editor_function(input_files: EditorInputFiles, output_files: SingleFile) -> None:
    resource_list_file = input_files["resources_pickle"]
    calculator_editor_html_filepath = output_files["file"]

    # Load and validate the type of the resource list data
    with open(resource_list_file, 'rb') as f:
        resource_list = pickle.load(f)
        if not isinstance(resource_list, ResourceList):
            raise ValueError("Pickled Resource List File is not a valid ResourceList class")

    env = Environment(loader=FileSystemLoader('core'))

    resource_list_js_data = mini_js_data(hack_update_resources_schema(get_primitive(resource_list)), "resource_list_json")

    editor_template = env.get_template("edit.html")

    rendered_editor = editor_template.render(
        resource_list_json=resource_list_js_data,
        element_height=55,  # should be automatically generated from the image height? width? or should be static
        total_height=55 * 989,  # Should be implemented in-javascript
        buffer_element_count=2,
    )

    # TODO: Minify this editor page at some point

    with open(calculator_editor_html_filepath, "w", encoding="utf_8") as f:
        f.write(rendered_editor)


################################################################################
# hack_update_resources_schema
#
# Temporary file to update the resource file to the new format that does not
# use ordered dictionaries and instead uses arrays of dictionaries.
################################################################################
def hack_update_resources_schema(data: Any) -> Any:
    new_authors = []
    for author in data["authors"]:
        new_authors.append({
            "name": author,
            "link": data["authors"][author]
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
