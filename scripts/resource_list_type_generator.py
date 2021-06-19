import sys
from typing import List


class Variable():
    def __init__(
        self,
        name: str,
        type: str,
        default: str,
        # required: bool = False,
    ) -> None:
        self.name = name
        self.type = type
        self.default = default


def generate_class(classname: str, variables: List[Variable]) -> None:
    print()
    print()
    print("# Class Generated with resource_list_type_generator.py")
    print("class {}():".format(classname))
    print("    def __init__(self) -> None:")

    for variable in variables:
        print("        self.{}: {} = {}".format(variable.name, variable.type, variable.default))

    print("")
    print("        self.valid_keys = {}".format(str([v.name for v in variables])))
    print("")
    print("    def parse(self, tuple_tree: Any) -> List[TokenError]:")
    print("        errors: List[TokenError] = []")
    print("")
    print("        # Create error for invalid keys")
    print("        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):")
    print("            errors.append(TokenError(\"Found Invalid {name} key, valid {name} keys are {{}}\".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))".format(name=classname))
    print("")
    print("        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}")

    for variable in variables:
        varblock = []

        varblock.append("")
        varblock.append("        # Load {name} into a typed object")
        varblock.append("        if '{}' in tokenless_keys:".format(variable.name))

        if variable.type == "str":
            varblock.append("            {name} = tokenless_keys[\"{name}\"]")
            varblock.append("            if type({name}.value) != str:")
            varblock.append("                errors.append(TokenError(\"{name} should be a string not a {{}}\".format(str(type({name}.value))), Token().from_yaml_scalar_node({name}.token)))")
            varblock.append("")
            varblock.append("            self.{name} = str({name}.value)")
        elif variable.type == "Optional[str]":
            varblock.append("            {name} = tokenless_keys[\"{name}\"]")
            varblock.append("            if {name}.value is not None:")
            varblock.append("                if type({name}.value) != str:")
            varblock.append("                    errors.append(TokenError(\"{name} should be a string not a {{}}\".format(str(type({name}.value))), Token().from_yaml_scalar_node({name}.token)))")
            varblock.append("")
            varblock.append("                self.{name} = str({name}.value)")
        elif variable.type.startswith("OrderedDict["):
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
                varblock.append("                self.{name}[str(key.value)] = int(value.value)")
            elif variable.type == "OrderedDict[str, StackSize]":
                varblock += subobject_parse("StackSize")

            elif variable.type == "OrderedDict[str, Resource]":
                varblock += subobject_parse("Resource")

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
            varblock.append("            self.{name} = int({name}.value)")
        elif variable.type == "List[Recipe]":
            varblock.append("            for item in tokenless_keys['{name}']:")
            varblock.append("                recipe = Recipe()")
            varblock.append("                errors += recipe.parse(item)")
            varblock.append("                self.{name}.append(recipe)")

        else:
            print("UNKNOWN VARIABLE TYPE", variable.type, file=sys.stderr)

        print("\n".join(varblock).format(name=variable.name))

    print("        return errors")
    print()
    print("    def to_primitive(self) -> Any:")
    print("        return {")
    for variable in variables:
        print("            \"{name}\": get_primitive(self.{name}),".format(name=variable.name))
    print("        }")


def subobject_parse(object_name: str) -> List[str]:
    chunk = []
    chunk.append("                " + object_name + "_subobject = " + object_name + "()")
    chunk.append("                errors += " + object_name + "_subobject.parse(value)")
    chunk.append("")
    chunk.append("                self.{name}[str(key.value)] = " + object_name + "_subobject")
    return chunk


generate_class(
    classname="ResourceList",
    variables=[
        Variable(
            name="authors",
            type="OrderedDict[str, str]",
            default="OrderedDict()"
        ),
        Variable(
            name="index_page_display_name",
            type="str",
            default='""'
        ),
        Variable(
            name="recipe_types",
            type="OrderedDict[str, str]",
            default="OrderedDict()"
        ),
        Variable(
            name="stack_sizes",
            type="OrderedDict[str, StackSize]",
            default="OrderedDict()"
        ),
        Variable(
            name="default_stack_size",
            type="str",
            default='""'
        ),
        Variable(
            name="resources",
            type="OrderedDict[str, Resource]",
            default="OrderedDict()"
        ),
        Variable(
            name="game_version",
            type="str",
            default='""'
        ),
        Variable(
            name="banner_message",
            type="str",
            default='""'
        ),
        Variable(
            name="requirement_groups",
            type="OrderedDict[str, List[str]]",
            default="OrderedDict()"
        ),
        Variable(
            name="row_group_count",
            type="int",
            default="1",
        )
    ]
)


generate_class(
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
            type="OrderedDict[str, int]",
            default="OrderedDict()",
        )
    ]
)


generate_class(
    classname="Resource",
    variables=[
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
        Variable(
            name="custom_simplename",
            type="str",
            default='""',
        ),
    ]
)

generate_class(
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
            type="OrderedDict[str, int]",
            default="OrderedDict()"
        )
    ]
)
