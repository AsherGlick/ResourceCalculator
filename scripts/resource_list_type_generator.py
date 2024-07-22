import sys
from typing import List, Tuple, Literal, Union
import shutil
from dataclasses import dataclass

VariableType_Scalar = Union[Literal["str"], Literal["int"]]
VariableType_OrderedDict = Tuple[Literal["OrderedDict"], "VariableType", "VariableType"]
VariableType_List = Tuple[Literal["List"], "VariableType"]
VariableType = Union[VariableType_Scalar, VariableType_OrderedDict]

a: VariableType = ("OrderedDict", "str", ("OrderedDict", "str", "str"))


def main() -> None:
    classes: List[Class] = [
        Class(
            classname="ResourceList",
            variables=[
                Variable(
                    name="authors",
                    type="OrderedDict[str, str]",
                    default="OrderedDict()",
                ),
                Variable(
                    name="index_page_display_name",
                    type="str",
                    default='""',
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="game_version",
                    type="str",
                    default='""',
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="row_group_count",
                    type="int",
                    default="1",
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="note",
                    type="str",
                    default='""',
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="banner_message",
                    type="str",
                    default='""',
                    blank_lines_above_field=1,
                ),

                Variable(
                    name="recipe_types",
                    type="OrderedDict[str, str]",
                    default="OrderedDict()",
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="requirement_groups",
                    type="OrderedDict[str, List[str]]",
                    default="OrderedDict()",
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="stack_sizes",
                    type="OrderedDict[str, StackSize]",
                    default="OrderedDict()",
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="default_stack_size",
                    type="str",
                    default='""',
                    blank_lines_above_field=1,
                ),
                Variable(
                    name="resources",
                    type="OrderedDict[str, Union[Resource, Heading]]",
                    default="OrderedDict()",
                    blank_lines_above_field=1,
                ),
            ]
        ),


        Class(
            classname="StackSize",
            variables=[
                Variable(
                    name="quantity_multiplier",
                    type="int",
                    default="0"
                ),
                Variable(
                    name="note",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="plural",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="extends_from",
                    type="Optional[str]",
                    default="None",
                    always_present=True,
                ),

                # custom_multipliers is a piece of data that is filled in via
                # Resource.custom_stack_multipliers, but it lives here for lookup
                Variable(
                    name="custom_multipliers",
                    type="OrderedDict[str, int]",
                    default="OrderedDict()",
                )
            ]
        ),


        Class(
            classname="Resource",
            variables=[
                Variable(
                    name="custom_simplename",
                    type="str",
                    default='""',
                ),
                Variable(
                    name="currency",
                    type="bool",
                    default="False"
                ),
                Variable(
                    name="note",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="recipes",
                    type="List[Recipe]",
                    default="[]"
                ),
                Variable(
                    name="custom_stack_multipliers",
                    type="OrderedDict[str, int]",
                    default="OrderedDict()"
                ),
            ]
        ),
        Class(
            classname="Heading",
            variables=[
                Variable(
                    name="H1",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="H2",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="H3",
                    type="str",
                    default='""'
                )
            ]
        ),
        Class(
            classname="Recipe",
            variables=[
                Variable(
                    name="output",
                    type="int",
                    default="0",
                ),
                Variable(
                    name="recipe_type",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="note",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="requirements",
                    type="OrderedDict[str, int]",
                    default="OrderedDict()"
                ),
            ]
        )
    ]

    generate_python_parser_classes(classes)

    new_classes: List[Class] = [
        Class(
            classname="ResourceList",
            variables=[
                Variable(
                    name="authors",
                    type="List[Author]",
                    default="{}"
                ),
                Variable(
                    name="index_page_display_name",
                    type="str",
                    default='""',
                    line_above=True,  # Formatting Style
                ),
                Variable(
                    name="row_group_count",
                    type="int",
                    default="1",
                    line_above=True,  # Formatting Style
                ),
                Variable(
                    name="game_version",
                    type="str",
                    default='""',
                    line_above=True,  # Formatting Style
                ),
                Variable(
                    name="banner_message",
                    type="str",
                    default='""',
                    line_above=True,  # Formatting Style
                ),
                Variable(
                    name="recipe_types",
                    type="Dict[str, str]",
                    default="{}",
                    line_above=True,  # Formatting Style
                ),
                Variable(
                    name="requirement_groups",
                    type="Dict[str, List[str]]",
                    default="{}",
                    line_above=True,  # Formatting Style
                    split_elems=True,  # Formatting Style
                ),
                Variable(
                    name="stack_sizes",
                    type="Dict[str, StackSize]",
                    default="{}",
                    line_above=True,  # Formatting Style
                ),
                Variable(
                    name="default_stack_size",
                    type="str",
                    default='""',
                    line_above=True,  # Formatting Style
                ),
                Variable(
                    name="resources",
                    type="List[Resource]",
                    default="{}",
                    line_above=True,  # Formatting Style
                    split_elems=True,  # Formatting Style
                ),
            ]
        ),


        Class(
            classname="StackSize",
            variables=[
                Variable(
                    name="quantity_multiplier",
                    type="int",
                    default="0"
                ),
                Variable(
                    name="plural",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="extends_from",
                    type="Optional[str]",
                    default="None"
                ),
                # custom_multipliers is a piece of data that is filled in via
                # Resource.custom_stack_multipliers, but it lives here for lookup
                Variable(
                    name="custom_multipliers",
                    type="Dict[str, int]",
                    default="{}",
                    ephemeral=True,
                )
            ]
        ),


        Class(
            classname="Resource",
            variables=[
                Variable(
                    name="name",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="id",
                    type="int",
                    default="-1"
                ),
                Variable(
                    name="recipes",
                    type="List[Recipe]",
                    default="[]"
                ),
                Variable(
                    name="custom_stack_multipliers",
                    type="Dict[str, int]",
                    default="{}"
                ),
                Variable(
                    name="custom_simplename",
                    type="str",
                    default='""',
                ),
                Variable(
                    name="currency",
                    type="bool",
                    default="False"
                ),
            ]
        ),

        Class(
            classname="Recipe",
            variables=[
                Variable(
                    name="output",
                    type="int",
                    default="0",
                ),
                Variable(
                    name="recipe_type",
                    type="str",
                    default='""'
                ),
                Variable(
                    name="requirements",
                    type="Dict[str, int]",
                    default="{}"
                )
            ]
        ),

        Class(
            classname="Author",
            variables=[
                Variable(
                    name="name",
                    type="str",
                    default="\"\""
                ),
                Variable(
                    name="link",
                    type="str",
                    default="\"\""
                )
            ]
        )
    ]

    generate_javascript_writers(new_classes)


################################################################################
# Safely replcaes text between a start token and an end token. When replacing
# a new file is created and then moved to replace the existing file so the
# existing file should never be left in a half-completed state.
#
# TODO: Sanity check tokens to make sure they both exist once and that the start
# token exists before the end token.
################################################################################
def replace_text(starting_token: str, ending_token: str, new_text: str, filepath: str) -> None:
    tmp_filepath: str = filepath + "_tmp"

    with open(filepath, "r") as f:
        text = f.read()
        start_location = text.find(starting_token) + len(starting_token)
        end_location = text.find(ending_token)

        with open(tmp_filepath, "w") as tmp_file:
            tmp_file.write(text[0:start_location])
            tmp_file.write(new_text)
            tmp_file.write(text[end_location:])

    shutil.move(tmp_filepath, filepath)


################################################################################
# A data class to hold all the relevent fields to define a variable
################################################################################
@dataclass
class Variable():
    name: str
    type: str
    default: str

    blank_lines_above_field: int = 0
    always_present: bool = False

    # Old Variables
    ephemeral: bool = False
    line_above: bool = False
    split_elems: bool = False  # Style for Lists


################################################################################
# A data class to hold all the relevent fields to define a class
################################################################################
class Class():
    def __init__(
        self,
        classname: str,
        variables: List[Variable]
    ) -> None:
        self.classname = classname
        self.variables = variables


def generate_javascript_writers(classes: List[Class]) -> None:
    javascript_writers: List[str] = []
    for javascript_writer in classes:
        javascript_writers.append(generate_javascript_writer(javascript_writer.classname, javascript_writer.variables))

    javascript_code_text = "\n".join(javascript_writers)

    replace_text("// BEGINGENERATOR", "// ENDGENERATOR", javascript_code_text, "../core/yaml_export.js")


def generate_javascript_writer(classname: str, variables: List[Variable]) -> str:
    lines: List[str] = []

    lines.append("")
    lines.append("function write_{}(object, indented=0){{".format(classname))
    lines.append("    let output = \"\";")
    lines.append('    const tab = "  ";')
    lines.append('    let indent = tab.repeat(indented);')

    variable_name_list: str = ",".join(["\"" + variable.name + "\"" for variable in variables])
    lines.append("    const key_list = [{}];".format(variable_name_list))

    # Validate we have no extra keys
    lines.append("    const key_set = new Set(key_list);")
    lines.append("    let key_names = Object.keys(object);")
    lines.append("    for (var i in key_names) {")
    lines.append("        let key_name = key_names[i];")
    lines.append("        if (!key_set.has(key_name)) {")
    lines.append('            console.warn("Unknown Key Found " + key_name);')
    lines.append("        }")
    lines.append("    }")

    # Write out each variable
    for variable in variables:

        # Skip writing ephermeral variables
        if variable.ephemeral:
            continue

        lines.append("    if (\"{}\" in object) {{".format(variable.name))

        if variable.line_above:
            lines.append('        output += "\\n"')

        lines.append('        output += indent + "{}:"'.format(variable.name))

        varblock = []

        if variable.type == "str":
            varblock.append('        output += " \\"" + object["{name}"] + "\\"\\n";')
        elif variable.type == "int":
            varblock.append('        output += " " + object[\"{name}\"] + "\\n";')
        elif variable.type == "bool":
            varblock.append('        if (object[\"{name}\"]) {{')
            varblock.append('            output += " true\\n";')
            varblock.append('        }} else {{')
            varblock.append('            output += " false\\n";')
            varblock.append('        }}')
        elif variable.type == "Optional[str]":
            varblock.append('        if (object["{name}"] == null) {{')
            varblock.append('            output += " null\\n";')
            varblock.append('        }} else {{')
            varblock.append('            output += " \\"" + object["{name}"] + "\\"\\n";')
            varblock.append('        }}')
        elif variable.type.startswith("Dict["):
            if not variable.split_elems:
                varblock.append('        output += "\\n";')

            varblock.append('        for (let dict_key in object["{name}"]) {{')

            if variable.split_elems:
                varblock.append('            output += "\\n"')

            # TODO we can probably split up the key and value pairs here to make logic cleaner
            if variable.type == "Dict[str, str]":
                varblock.append('            output += indent + tab + dict_key + ": \\"" + object["{name}"][dict_key] + "\\"\\n";')
            elif variable.type == "Dict[str, int]":
                varblock.append('              output += indent + tab + dict_key + ": " + object["{name}"][dict_key] + "\\n";')
            elif variable.type == "Dict[str, StackSize]":
                varblock.append('              output += indent + tab + dict_key + ":\\n" + write_' + "StackSize" + '( object["{name}"][dict_key], indented+2);')

            elif variable.type == "Dict[str, List[str]]":
                varblock.append('              output += indent + tab + dict_key + ":\\n";')
                varblock.append('              for (let list_index in object["{name}"][dict_key]) {{')
                varblock.append('                  output +=  indent + tab + tab + "- " + object["{name}"][dict_key][list_index] + "\\n"')
                varblock.append('              }}')
            else:
                print("UNKNOWN JAVASCRIPT WRITER VARIABLE TYPE", variable.type, file=sys.stderr)

            varblock.append('        }}')

        elif variable.type.startswith("List["):
            if not variable.split_elems:
                varblock.append('        output += "\\n";')
            varblock.append('        for (let list_index in object["{name}"]) {{')

            if variable.split_elems:
                varblock.append('            output += "\\n"')

            if variable.type == "List[Resource]":
                varblock.append('        output += indent + tab + "- " + write_Resource(object["{name}"][list_index], indented+2).trim() + "\\n";')
            elif variable.type == "List[Recipe]":
                varblock.append('        output += indent + tab + "- " + write_Recipe(object["{name}"][list_index], indented+2).trim() + "\\n";')
            elif variable.type == "List[Author]":
                varblock.append('        output += indent + tab + "- " + write_Author(object["{name}"][list_index], indented+2).trim() + "\\n";')

            else:
                print("UNKNOWN JAVASCRIPT WRITER VARIABLE TYPE", variable.type, file=sys.stderr)
            varblock.append('        }}')

        else:
            print("UNKNOWN JAVASCRIPT WRITER VARIABLE TYPE", variable.type, file=sys.stderr)

        lines.append("\n".join(varblock).format(name=variable.name))

        lines.append("    }")

    lines.append("    return output;")
    lines.append("}")
    lines.append("")

    return "\n".join(lines)


def generate_python_parser_classes(classes: List[Class]) -> None:
    python_classes: List[str] = []
    for python_class in classes:
        python_classes.append(generate_python_parser_class(python_class.classname, python_class.variables))

    python_code_text = "\n".join(python_classes)

    replace_text("# BEGINGENERATOR", "# ENDGENERATOR", python_code_text, "../pylib/resource_list.py")


def generate_python_parser_class(classname: str, variables: List[Variable]) -> str:

    lines: List[str] = []

    lines.append("")
    lines.append("# Class Generated with resource_list_type_generator.py")
    lines.append("class {}():".format(classname))
    lines.append("    def __init__(self) -> None:")

    for variable in variables:
        lines.append("        self.{}: {} = {}".format(variable.name, variable.type, variable.default))

    lines.append("")
    lines.append("        self.valid_keys = {}".format(str([v.name for v in variables])))
    lines.append("")
    lines.append("    def parse(self, tuple_tree: Any) -> List[TokenError]:")
    lines.append("        errors: List[TokenError] = []")
    lines.append("")
    lines.append("        # Create error for invalid keys")
    lines.append("        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):")
    lines.append("            errors.append(TokenError(\"Found Invalid {name} key, valid {name} keys are {{}}\".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))".format(name=classname))
    lines.append("")

    lines.append("        # Create error for duplicate keys")
    lines.append("        for duplicate_key in _get_duplicate_keys(tuple_tree):")
    lines.append("            errors.append(TokenError(\"Found Duplicate {name} key\", Token().from_yaml_scalar_node(duplicate_key.token)))".format(name=classname))
    lines.append("")

    lines.append("        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}")

    for variable in variables:
        varblock: List[str] = []

        varblock.append("")
        varblock.append("        # Load {name} into a typed object")
        varblock.append("        if '{}' in tokenless_keys:".format(variable.name))

        if variable.type == "str":
            varblock.append("            {name} = tokenless_keys[\"{name}\"]")
            varblock.append("            if type({name}.value) != str:")
            varblock.append("                errors.append(TokenError(\"{name} should be a string not a {{}}\".format(str(type({name}.value))), Token().from_yaml_scalar_node({name}.token)))")
            varblock.append("")
            varblock.append("            self.{name} = str({name}.value)")
        elif variable.type == "bool":
            varblock.append("            {name} = tokenless_keys[\"{name}\"]")
            varblock.append("            if type({name}.value) != bool:")
            varblock.append("                errors.append(TokenError(\"{name} should be a bool not a {{}}\".format(str(type({name}.value))), Token().from_yaml_scalar_node({name}.token)))")
            varblock.append("")
            varblock.append("            self.{name} = bool({name}.value)")
            pass
        elif variable.type == "Optional[str]":
            varblock.append("            {name} = tokenless_keys[\"{name}\"]")
            varblock.append("            if {name}.value is not None:")
            varblock.append("                if type({name}.value) != str:")
            varblock.append("                    errors.append(TokenError(\"{name} should be a string not a {{}}\".format(str(type({name}.value))), Token().from_yaml_scalar_node({name}.token)))")
            varblock.append("")
            varblock.append("                self.{name} = str({name}.value)")
        elif variable.type.startswith("OrderedDict["):
            varblock.append("            # Create error for duplicate keys")
            varblock.append("            for duplicate_key in _get_duplicate_keys(tokenless_keys[\"{name}\"]):")
            varblock.append("                errors.append(TokenError(\"Found Duplicate {name} key\", Token().from_yaml_scalar_node(duplicate_key.token)))")
            varblock.append("")
            varblock.append("            for key, value in tokenless_keys[\"{name}\"].items():")
            varblock.append("                if type(key.value) != str:")
            varblock.append("                    errors.append(TokenError(\"{name} key should be a string not a {{}}\".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))")
            varblock.append("")

            if variable.type == "OrderedDict[str, str]":
                varblock.append("                if type(value.value) != str:")
                varblock.append("                    errors.append(TokenError(\"{name} value should be a string not a {{}}\".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))")
                varblock.append("")
                varblock.append("                self.{name}[str(key.value)] = str(value.value)")
            elif variable.type == "OrderedDict[str, int]":
                varblock.append("                if type(value.value) != int:")
                varblock.append("                    errors.append(TokenError(\"{name} value should be an int not a {{}}\".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))")
                varblock.append("")
                varblock.append("                self.{name}[str(key.value)] = int(value.value or 0)")
            elif variable.type == "OrderedDict[str, StackSize]":
                varblock += subobject_parse_python("StackSize")

            elif variable.type == "OrderedDict[str, Union[Resource, Heading]]":
                varblock.append("                tokenless_value_keys = [x.value for x in value.keys()]")
                varblock.append("                if 'H1' in tokenless_value_keys or 'H2' in tokenless_value_keys or 'H3' in tokenless_value_keys:")
                varblock += subobject_parse_python("Heading", 20)
                varblock.append("                else:")
                varblock += subobject_parse_python("Resource", 20)

            elif variable.type == "OrderedDict[str, List[str]]":
                varblock.append("                item_list: List[str] = []")
                varblock.append("                for item in value:")
                varblock.append("                    if type(item.value) != str:")
                varblock.append("                        errors.append(TokenError(\"{name} element should be a string not a {{}}\".format(str(type(item.value))), Token().from_yaml_scalar_node(item.token)))")
                varblock.append("                    item_list.append(str(item.value))")
                varblock.append("                self.{name}[str(key.value)] = item_list")
            else:
                print("UNKNOWN VARIABLE TYPE", variable.type, file=sys.stderr)
        elif variable.type == "int":
            varblock.append("            {name} = tokenless_keys[\"{name}\"]")
            varblock.append("            if type({name}.value) != int:")
            varblock.append("                errors.append(TokenError(\"{name} should be an int not a {{}}\".format(str(type({name}.value))), Token().from_yaml_scalar_node({name}.token)))")
            varblock.append("")
            varblock.append("            self.{name} = int({name}.value or 0)")
        elif variable.type == "List[Recipe]":
            varblock.append("            for item in tokenless_keys['{name}']:")
            varblock.append("                recipe = Recipe()")
            varblock.append("                errors += recipe.parse(item)")
            varblock.append("                self.{name}.append(recipe)")

        else:
            print("UNKNOWN VARIABLE TYPE", variable.type, file=sys.stderr)

        lines.append("\n".join(varblock).format(name=variable.name))

    lines.append("        return errors")
    lines.append("")
    lines.append("    def to_primitive(self) -> Any:")
    lines.append("        return {")
    for variable in variables:
        lines.append("            \"{name}\": get_primitive(self.{name}),".format(name=variable.name))
    lines.append("        }")
    lines.append("")

    lines.append("    def to_yaml(self, indent: str = \"\") -> str:")
    lines.append("        output = []")
    for variable in variables:
        indent = ""

        varblock = []

        if not variable.always_present:
            if variable.type == "bool":
                varblock.append("        if self.{name} is " + variable.default + ":")
            else:
                varblock.append("        if self.{name} != " + variable.default + ":")
            indent = "    "

        for _ in range(variable.blank_lines_above_field):
            varblock.append(indent + "        output.append(\"\")")

        if variable.type == "str":
            varblock.append(indent + "        output.append(indent + \"{name}: \" + yaml_string(self.{name}, indent))")
        elif variable.type == "bool":
            varblock.append(indent + "        output.append(indent + \"{name}: \" + str(self.{name}))")
        elif variable.type == "Optional[str]":
            if variable.default is not None or variable.always_present is True:
                varblock.append(indent + "        if self.{name} is None:")
                varblock.append(indent + "            output.append(indent + \"{name}: null\")")
                varblock.append(indent + "        else:")
                varblock.append(indent + "            output.append(indent + \"{name}: \" + yaml_string(self.{name}, indent))")
            else:
                varblock.append(indent + "        output.append(indent + \"{name}: \" + yaml_string(self.{name}, indent))")

        elif variable.type == "OrderedDict[str, str]":
            varblock.append(indent + "        output.append(indent + \"{name}:\")")
            varblock.append(indent + "        for {name}_k, {name}_v in self.{name}.items():")
            varblock.append(indent + "            output.append(indent + \"  \" + {name}_k + \": \" + yaml_string({name}_v, indent + \"  \"))")
        elif variable.type == "OrderedDict[str, int]":
            varblock.append(indent + "        output.append(indent + \"{name}:\")")
            varblock.append(indent + "        for {name}_k, {name}_v in self.{name}.items():")
            varblock.append(indent + "            output.append(indent + \"  \" + {name}_k + \": \" + str({name}_v))")
        elif variable.type == "OrderedDict[str, StackSize]":
            varblock.append(indent + "        output.append(\"{name}:\")")
            varblock.append(indent + "        for {name}_k, {name}_v in self.{name}.items():")
            varblock.append(indent + "            output.append(indent + \"  \" + {name}_k + \":\")")
            varblock.append(indent + "            output.append({name}_v.to_yaml(indent + '    '))")

        elif variable.type == "OrderedDict[str, Union[Resource, Heading]]":
            varblock.append(indent + "        output.append(\"{name}:\")")
            varblock.append(indent + "        for i, ({name}_k, {name}_v) in enumerate(self.{name}.items()):")
            varblock.append(indent + "            if isinstance({name}_v, Resource):")
            varblock.append(indent + "                if i != 0:")
            varblock.append(indent + "                    output.append(\"\")")
            varblock.append(indent + "                output.append(indent + \"  \" + {name}_k + \":\")")
            varblock.append(indent + "                output.append({name}_v.to_yaml(indent + '    '))")
            varblock.append("")
            varblock.append(indent + "            elif isinstance({name}_v, Heading):")
            varblock.append(indent + "                if {name}_v.H1 != \"\":")
            varblock.append(indent + "                    output.append(\"\")")
            varblock.append(indent + "                    output.append(indent + \"  \" + \"#\" * (78 - len(indent)))")
            varblock.append(indent + "                    line = indent + \"  \" + {name}_k + \": {{H1: \" + {name}_v.H1 + \"}}\"")
            varblock.append(indent + "                    line += \" \" + \"#\" * (79 - len(line))")
            varblock.append(indent + "                    output.append(line)")
            varblock.append(indent + "                    output.append(indent + \"  \" + \"#\" * (78 - len(indent)))")
            varblock.append(indent + "                elif {name}_v.H2 != \"\":")
            varblock.append(indent + "                    output.append(\"\")")
            varblock.append(indent + "                    line = indent + \"  \" + {name}_k + \": {{H2: \" + {name}_v.H2 + \"}}\"")
            varblock.append(indent + "                    line += \" \" + \"#\" * (79 - len(line))")
            varblock.append(indent + "                    output.append(line)")
            varblock.append(indent + "                elif {name}_v.H3 != \"\":")
            varblock.append(indent + "                    output.append(\"\")")
            varblock.append(indent + "                    output.append(indent + \"  \" + {name}_k + \": {{H3: \" + {name}_v.H3 + \"}}\")")
            varblock.append("")
            varblock.append(indent + "            else:")
            varblock.append(indent + "                raise ValueError")

        elif variable.type == "OrderedDict[str, List[str]]":
            varblock.append(indent + "        output.append(\"{name}:\")")
            varblock.append(indent + "        for i, ({name}_k, {name}_v) in enumerate(self.{name}.items()):")
            varblock.append(indent + "            if i != 0:")
            varblock.append(indent + "                output.append(\"\")")
            varblock.append(indent + "            output.append(indent + \"  \" + {name}_k + \":\")")
            varblock.append(indent + "            for item in {name}_v:")
            varblock.append(indent + "                output.append(indent + '  - ' + yaml_string(item, indent + '    '))")

        elif variable.type == "int":
            varblock.append(indent + "        output.append(indent + \"{name}: \" + str(self.{name}))")

        elif variable.type == "List[Recipe]":
            varblock.append(indent + "        output.append(indent + \"{name}:\")")
            varblock.append(indent + "        for {name}_v in self.{name}:")
            varblock.append(indent + "            line = {name}_v.to_yaml(indent + '  ')")
            varblock.append(indent + "            line = indent + '- ' + line.removeprefix(indent + '  ')")
            varblock.append(indent + "            output.append(line)")

        else:
            print("UNKNOWN VARIABLE TYPE", variable.type, file=sys.stderr)

        lines.append("\n".join(varblock).format(name=variable.name))

    lines.append("        return '\\n'.join(output)")

    lines.append("")

    return "\n".join(lines)


################################################################################
#
################################################################################
def subobject_parse_python(object_name: str, indent: int = 16) -> List[str]:
    chunk = []
    chunk.append(" " * indent + object_name + "_subobject = " + object_name + "()")
    chunk.append(" " * indent + "errors += " + object_name + "_subobject.parse(value)")
    chunk.append("")
    chunk.append(" " * indent + "self.{name}[str(key.value)] = " + object_name + "_subobject")
    return chunk


if __name__ == "__main__":
    main()
