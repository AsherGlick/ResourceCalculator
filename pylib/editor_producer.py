from jinja2 import Environment, FileSystemLoader
from typing import List, Dict, TypedDict
import os
import pickle

from pylib.json_data_compressor import mini_js_data
from pylib.producer import Producer, GenericProducer
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
            name="Build Editor page",
            input_path_patterns={
                "resources_pickle": r"^cache/(?P<calculator_dir>{calculator_dir_regex})/resources\.pickle$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
                "image_layout_json": r"^cache/(?P<calculator_dir>{calculator_dir_regex})/packed_image_layout\.json$".format(
                    calculator_dir_regex=calculator_dir_regex
                ),
                "editor_template": r"^core/edit\.html$",
            },
            function=editor_function,
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
# editor_function
#
# The processing function that generates the output editor file given a struct
# of input and output files via the producer.
################################################################################
def editor_function(input_files: EditorInputFiles, groups: Dict[str, str]) -> List[str]:
    resource_list_file = input_files["resources_pickle"]
    calculator_page = groups["calculator_dir"]
    calculator_editor_html_filepath = os.path.join("output", calculator_page, "edit.html")

    # Load and validate the type of the resource list data
    with open(resource_list_file, 'rb') as f:
        resource_list = pickle.load(f)
        if not isinstance(resource_list, ResourceList):
            raise ValueError("Pickled Resource List File is not a valid ResourceList class")

    env = Environment(loader=FileSystemLoader('core'))

    resource_list_js_data = mini_js_data(get_primitive(resource_list), "resource_list_json")

    editor_template = env.get_template("edit.html")

    rendered_editor = editor_template.render(
        resource_list_json=resource_list_js_data,
        element_height=55,  # should be automatically generated from the image height? width? or should be static
        total_height=55 * 989,  # Should be implemented in-javascript
        buffer_element_count=2,
    )

    # TODO: Minify this editor page at some point

    os.makedirs(os.path.dirname(calculator_editor_html_filepath), exist_ok=True)
    with open(calculator_editor_html_filepath, "w", encoding="utf_8") as f:
        f.write(rendered_editor)

    return [
        calculator_editor_html_filepath,
    ]
