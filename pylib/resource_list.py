from typing import List, Optional, Any, Union
import yaml
from collections import OrderedDict

from .yaml_token_load import TokenBundle


################################################################################
#
################################################################################
class Token():
    def __init__(
            self,
            start_line: int = 0,
            end_line: int = 0,
            start_column: int = 0,
            end_column: int = 0
    ) -> None:
        self.start_line: int = start_line
        self.end_line: int = end_line
        self.start_column: int = start_column
        self.end_column: int = end_column

    def from_yaml_scalar_node(self, token: yaml.nodes.ScalarNode) -> 'Token':
        self.start_line = token.start_mark.line
        self.end_line = token.end_mark.line
        self.start_column = token.start_mark.column
        self.end_column = token.end_mark.column
        return self

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "Token({}, {}, {}, {})".format(
            str(self.start_line),
            str(self.end_line),
            str(self.start_column),
            str(self.end_column),
        )

    def __eq__(self, other: Any) -> bool:
        if type(other) != Token:
            return False

        if (
            other.start_line == self.start_line
            and other.end_line == self.end_line
            and other.start_column == self.start_column
            and other.end_column == self.end_column
        ):
            return True
        return False


class TokenError():
    def __init__(self, error_string: str, token: Token) -> None:
        self.error_string: str = error_string
        self.token: Token = token

    def print_error(self, raw_text: List[str]) -> None:
        start_line_number = self.token.start_line
        end_line_number = self.token.end_line

        start_column = self.token.start_column
        end_column = self.token.end_column

        if start_line_number == end_line_number:
            print("Line \033[92m{}\033[0m: {}".format(
                str(start_line_number + 1),
                self.error_string,
            ))

            print(" │{}\033[91m{}\033[0m{}".format(
                raw_text[start_line_number][0:start_column],
                raw_text[start_line_number][start_column:end_column],
                raw_text[start_line_number][end_column:],
            ))

            print(" │{}\033[91m{}\033[0m".format(
                " " * (start_column),
                "^" * (end_column - start_column),
            ))

        else:
            print("Multi Line Error (Printing Not Yet Supported)")

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        return "TokenError(" + repr(self.error_string) + ", " + str(self.token) + ")"

    def __eq__(self, other: Any) -> bool:
        if type(other) != TokenError:
            return False
        if self.error_string == other.error_string and self.token == other.token:
            return True
        return False


################################################################################
# A helper function to call the "to_primitive()" function on a nested series
# of classes in order to return an object that can easily be serialized.
################################################################################
def get_primitive(obj: Any) -> Any:
    if type(obj) == list:
        return [get_primitive(x) for x in obj]
    elif type(obj) == dict:
        return {k: get_primitive(v) for k, v in obj.items()}
    elif type(obj) == OrderedDict:
        return {k: get_primitive(v) for k, v in obj.items()}
        # return OrderedDict([(k, get_primitive(v)) for k, v in obj.items()])
    elif hasattr(obj, "to_primitive"):
        return obj.to_primitive()
    else:
        return obj


################################################################################
# yaml_string
#
# A helper function to print yaml string values out
################################################################################
def yaml_string(string: str, indent: str):
    if "\n" in string:
        string = string.removesuffix("\n")
        return ("\n  " + indent).join(["|"] + string.split("\n"))

    if ":" in string:
        return '"' + string.replace('\\', '\\\\').replace('"', '\\"') + '"'

    if '"' in string:
        return '"' + string.replace('\\', '\\\\').replace('"', '\\"') + '"'

    if "'" in string:
        return '"' + string + '"'

    if string == "":
        return '""'

    if string[0].isdigit():
        return '"' + string.replace('\\', '\\\\').replace('"', '\\"') + '"'

    return string

################################################################################
# _get_invalid_keys
#
# A helper function to list out all of the keys that are invalid.
################################################################################
def _get_invalid_keys(data: Any, valid_keys: List[str]) -> List[TokenBundle]:
    invalid_keys: List[TokenBundle] = []

    for key in data:
        if key.value not in valid_keys:
            invalid_keys.append(key)

    return invalid_keys


################################################################################
# _get_duplicate_keys
#
# A helper function to list out any duplicate keys
################################################################################
def _get_duplicate_keys(data: Any) -> List[TokenBundle]:
    duplicate_keys: List[TokenBundle] = []
    seen_keys = set([])
    for key in data:
        if key.value in seen_keys:
            duplicate_keys.append(key)
        seen_keys.add(key.value)
    return duplicate_keys


################################################################################
################################ Generated Code ################################
################################################################################
# BEGINGENERATOR
# Class Generated with resource_list_type_generator.py
class ResourceList():
    def __init__(self) -> None:
        self.authors: OrderedDict[str, str] = OrderedDict()
        self.index_page_display_name: str = ""
        self.game_version: str = ""
        self.row_group_count: int = 1
        self.note: str = ""
        self.banner_message: str = ""
        self.recipe_types: OrderedDict[str, str] = OrderedDict()
        self.requirement_groups: OrderedDict[str, List[str]] = OrderedDict()
        self.stack_sizes: OrderedDict[str, StackSize] = OrderedDict()
        self.default_stack_size: str = ""
        self.resources: OrderedDict[str, Union[Resource, Heading]] = OrderedDict()

        self.valid_keys = ['authors', 'index_page_display_name', 'game_version', 'row_group_count', 'note', 'banner_message', 'recipe_types', 'requirement_groups', 'stack_sizes', 'default_stack_size', 'resources']

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # Create error for invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found Invalid ResourceList key, valid ResourceList keys are {}".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))

        # Create error for duplicate keys
        for duplicate_key in _get_duplicate_keys(tuple_tree):
            errors.append(TokenError("Found Duplicate ResourceList key", Token().from_yaml_scalar_node(duplicate_key.token)))

        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}

        # Load authors into a typed object
        if 'authors' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["authors"]):
                errors.append(TokenError("Found Duplicate authors key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["authors"].items():
                if type(key.value) != str:
                    errors.append(TokenError("authors key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != str:
                    errors.append(TokenError("authors value should be a string not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.authors[str(key.value)] = str(value.value)

        # Load index_page_display_name into a typed object
        if 'index_page_display_name' in tokenless_keys:
            index_page_display_name = tokenless_keys["index_page_display_name"]
            if type(index_page_display_name.value) != str:
                errors.append(TokenError("index_page_display_name should be a string not a {}".format(str(type(index_page_display_name.value))), Token().from_yaml_scalar_node(index_page_display_name.token)))

            self.index_page_display_name = str(index_page_display_name.value)

        # Load game_version into a typed object
        if 'game_version' in tokenless_keys:
            game_version = tokenless_keys["game_version"]
            if type(game_version.value) != str:
                errors.append(TokenError("game_version should be a string not a {}".format(str(type(game_version.value))), Token().from_yaml_scalar_node(game_version.token)))

            self.game_version = str(game_version.value)

        # Load row_group_count into a typed object
        if 'row_group_count' in tokenless_keys:
            row_group_count = tokenless_keys["row_group_count"]
            if type(row_group_count.value) != int:
                errors.append(TokenError("row_group_count should be an int not a {}".format(str(type(row_group_count.value))), Token().from_yaml_scalar_node(row_group_count.token)))

            self.row_group_count = int(row_group_count.value or 0)

        # Load note into a typed object
        if 'note' in tokenless_keys:
            note = tokenless_keys["note"]
            if type(note.value) != str:
                errors.append(TokenError("note should be a string not a {}".format(str(type(note.value))), Token().from_yaml_scalar_node(note.token)))

            self.note = str(note.value)

        # Load banner_message into a typed object
        if 'banner_message' in tokenless_keys:
            banner_message = tokenless_keys["banner_message"]
            if type(banner_message.value) != str:
                errors.append(TokenError("banner_message should be a string not a {}".format(str(type(banner_message.value))), Token().from_yaml_scalar_node(banner_message.token)))

            self.banner_message = str(banner_message.value)

        # Load recipe_types into a typed object
        if 'recipe_types' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["recipe_types"]):
                errors.append(TokenError("Found Duplicate recipe_types key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["recipe_types"].items():
                if type(key.value) != str:
                    errors.append(TokenError("recipe_types key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != str:
                    errors.append(TokenError("recipe_types value should be a string not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.recipe_types[str(key.value)] = str(value.value)

        # Load requirement_groups into a typed object
        if 'requirement_groups' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["requirement_groups"]):
                errors.append(TokenError("Found Duplicate requirement_groups key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["requirement_groups"].items():
                if type(key.value) != str:
                    errors.append(TokenError("requirement_groups key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                item_list: List[str] = []
                for item in value:
                    if type(item.value) != str:
                        errors.append(TokenError("requirement_groups element should be a string not a {}".format(str(type(item.value))), Token().from_yaml_scalar_node(item.token)))
                    item_list.append(str(item.value))
                self.requirement_groups[str(key.value)] = item_list

        # Load stack_sizes into a typed object
        if 'stack_sizes' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["stack_sizes"]):
                errors.append(TokenError("Found Duplicate stack_sizes key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["stack_sizes"].items():
                if type(key.value) != str:
                    errors.append(TokenError("stack_sizes key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                StackSize_subobject = StackSize()
                errors += StackSize_subobject.parse(value)

                self.stack_sizes[str(key.value)] = StackSize_subobject

        # Load default_stack_size into a typed object
        if 'default_stack_size' in tokenless_keys:
            default_stack_size = tokenless_keys["default_stack_size"]
            if type(default_stack_size.value) != str:
                errors.append(TokenError("default_stack_size should be a string not a {}".format(str(type(default_stack_size.value))), Token().from_yaml_scalar_node(default_stack_size.token)))

            self.default_stack_size = str(default_stack_size.value)

        # Load resources into a typed object
        if 'resources' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["resources"]):
                errors.append(TokenError("Found Duplicate resources key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["resources"].items():
                if type(key.value) != str:
                    errors.append(TokenError("resources key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                tokenless_value_keys = [x.value for x in value.keys()]
                if 'H1' in tokenless_value_keys or 'H2' in tokenless_value_keys or 'H3' in tokenless_value_keys:
                    Heading_subobject = Heading()
                    errors += Heading_subobject.parse(value)

                    self.resources[str(key.value)] = Heading_subobject
                else:
                    Resource_subobject = Resource()
                    errors += Resource_subobject.parse(value)

                    self.resources[str(key.value)] = Resource_subobject
        return errors

    def to_primitive(self) -> Any:
        return {
            "authors": get_primitive(self.authors),
            "index_page_display_name": get_primitive(self.index_page_display_name),
            "game_version": get_primitive(self.game_version),
            "row_group_count": get_primitive(self.row_group_count),
            "note": get_primitive(self.note),
            "banner_message": get_primitive(self.banner_message),
            "recipe_types": get_primitive(self.recipe_types),
            "requirement_groups": get_primitive(self.requirement_groups),
            "stack_sizes": get_primitive(self.stack_sizes),
            "default_stack_size": get_primitive(self.default_stack_size),
            "resources": get_primitive(self.resources),
        }

    def to_yaml(self, indent: str = "") -> str:
        output = []
        if self.authors != OrderedDict():
            output.append(indent + "authors:")
            for k, v in self.authors.items():
                output.append(indent + "  " + k + ": " + yaml_string(v, indent + "  "))
        if self.index_page_display_name != "":
            output.append("")
            output.append(indent + "index_page_display_name: " + yaml_string(self.index_page_display_name, indent))
        if self.game_version != "":
            output.append("")
            output.append(indent + "game_version: " + yaml_string(self.game_version, indent))
        if self.row_group_count != 1:
            output.append("")
            output.append(indent + "row_group_count: " + str(self.row_group_count))
        if self.note != "":
            output.append("")
            output.append(indent + "note: " + yaml_string(self.note, indent))
        if self.banner_message != "":
            output.append("")
            output.append(indent + "banner_message: " + yaml_string(self.banner_message, indent))
        if self.recipe_types != OrderedDict():
            output.append("")
            output.append(indent + "recipe_types:")
            for k, v in self.recipe_types.items():
                output.append(indent + "  " + k + ": " + yaml_string(v, indent + "  "))
        if self.requirement_groups != OrderedDict():
            output.append("")
            output.append("requirement_groups:")
            for i, (k, v) in enumerate(self.requirement_groups.items()):
                if i != 0:
                    output.append("")
                output.append(indent + "  " + k + ":")
                for item in v:
                    output.append(indent + '  - ' + yaml_string(item, indent + '    '))
        if self.stack_sizes != OrderedDict():
            output.append("")
            output.append("stack_sizes:")
            for k, v in self.stack_sizes.items():
                output.append(indent + "  " + k + ":")
                output.append(v.to_yaml(indent + '    '))
        if self.default_stack_size != "":
            output.append("")
            output.append(indent + "default_stack_size: " + yaml_string(self.default_stack_size, indent))
        if self.resources != OrderedDict():
            output.append("")
            output.append("resources:")
            for i, (k, v) in enumerate(self.resources.items()):
                if isinstance(v, Resource):
                    if i != 0:
                        output.append("")
                    output.append(indent + "  " + k + ":")
                    output.append(v.to_yaml(indent + '    '))

                elif isinstance(v, Heading):
                    if v.H1 != "":
                        output.append("")
                        output.append(indent + "  " + "#" * (78-len(indent)))
                        line = indent + "  " + k + ": {H1: " + v.H1 + "}"
                        line += " " + "#" * (79-len(line))
                        output.append(line)
                        output.append(indent + "  " + "#" * (78-len(indent)))
                    elif v.H2 != "":
                        output.append("")
                        line = indent + "  " + k + ": {H2: " + v.H2 + "}"
                        line += " " + "#" * (79-len(line))
                        output.append(line)
                    elif v.H3 != "":
                        output.append("")
                        output.append(indent + "  " + k + ": {H3: " + v.H3 + "}")

                else:
                    raise ValueError
        return '\n'.join(output)


# Class Generated with resource_list_type_generator.py
class StackSize():
    def __init__(self) -> None:
        self.quantity_multiplier: int = 0
        self.note: str = ""
        self.plural: str = ""
        self.extends_from: Optional[str] = None
        self.custom_multipliers: OrderedDict[str, int] = OrderedDict()

        self.valid_keys = ['quantity_multiplier', 'note', 'plural', 'extends_from', 'custom_multipliers']

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # Create error for invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found Invalid StackSize key, valid StackSize keys are {}".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))

        # Create error for duplicate keys
        for duplicate_key in _get_duplicate_keys(tuple_tree):
            errors.append(TokenError("Found Duplicate StackSize key", Token().from_yaml_scalar_node(duplicate_key.token)))

        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}

        # Load quantity_multiplier into a typed object
        if 'quantity_multiplier' in tokenless_keys:
            quantity_multiplier = tokenless_keys["quantity_multiplier"]
            if type(quantity_multiplier.value) != int:
                errors.append(TokenError("quantity_multiplier should be an int not a {}".format(str(type(quantity_multiplier.value))), Token().from_yaml_scalar_node(quantity_multiplier.token)))

            self.quantity_multiplier = int(quantity_multiplier.value or 0)

        # Load note into a typed object
        if 'note' in tokenless_keys:
            note = tokenless_keys["note"]
            if type(note.value) != str:
                errors.append(TokenError("note should be a string not a {}".format(str(type(note.value))), Token().from_yaml_scalar_node(note.token)))

            self.note = str(note.value)

        # Load plural into a typed object
        if 'plural' in tokenless_keys:
            plural = tokenless_keys["plural"]
            if type(plural.value) != str:
                errors.append(TokenError("plural should be a string not a {}".format(str(type(plural.value))), Token().from_yaml_scalar_node(plural.token)))

            self.plural = str(plural.value)

        # Load extends_from into a typed object
        if 'extends_from' in tokenless_keys:
            extends_from = tokenless_keys["extends_from"]
            if extends_from.value is not None:
                if type(extends_from.value) != str:
                    errors.append(TokenError("extends_from should be a string not a {}".format(str(type(extends_from.value))), Token().from_yaml_scalar_node(extends_from.token)))

                self.extends_from = str(extends_from.value)

        # Load custom_multipliers into a typed object
        if 'custom_multipliers' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["custom_multipliers"]):
                errors.append(TokenError("Found Duplicate custom_multipliers key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["custom_multipliers"].items():
                if type(key.value) != str:
                    errors.append(TokenError("custom_multipliers key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != int:
                    errors.append(TokenError("custom_multipliers value should be an int not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.custom_multipliers[str(key.value)] = int(value.value or 0)
        return errors

    def to_primitive(self) -> Any:
        return {
            "quantity_multiplier": get_primitive(self.quantity_multiplier),
            "note": get_primitive(self.note),
            "plural": get_primitive(self.plural),
            "extends_from": get_primitive(self.extends_from),
            "custom_multipliers": get_primitive(self.custom_multipliers),
        }

    def to_yaml(self, indent: str = "") -> str:
        output = []
        if self.quantity_multiplier != 0:
            output.append(indent + "quantity_multiplier: " + str(self.quantity_multiplier))
        if self.note != "":
            output.append(indent + "note: " + yaml_string(self.note, indent))
        if self.plural != "":
            output.append(indent + "plural: " + yaml_string(self.plural, indent))
        if self.extends_from is None:
            output.append(indent + "extends_from: null")
        else:
            output.append(indent + "extends_from: " + yaml_string(self.extends_from, indent))
        if self.custom_multipliers != OrderedDict():
            output.append(indent + "custom_multipliers:")
            for k, v in self.custom_multipliers.items():
                output.append(indent + "  " + k + ": " + str(v))
        return '\n'.join(output)


# Class Generated with resource_list_type_generator.py
class Resource():
    def __init__(self) -> None:
        self.custom_simplename: str = ""
        self.currency: bool = False
        self.note: str = ""
        self.recipes: List[Recipe] = []
        self.custom_stack_multipliers: OrderedDict[str, int] = OrderedDict()

        self.valid_keys = ['custom_simplename', 'currency', 'note', 'recipes', 'custom_stack_multipliers']

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # Create error for invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found Invalid Resource key, valid Resource keys are {}".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))

        # Create error for duplicate keys
        for duplicate_key in _get_duplicate_keys(tuple_tree):
            errors.append(TokenError("Found Duplicate Resource key", Token().from_yaml_scalar_node(duplicate_key.token)))

        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}

        # Load custom_simplename into a typed object
        if 'custom_simplename' in tokenless_keys:
            custom_simplename = tokenless_keys["custom_simplename"]
            if type(custom_simplename.value) != str:
                errors.append(TokenError("custom_simplename should be a string not a {}".format(str(type(custom_simplename.value))), Token().from_yaml_scalar_node(custom_simplename.token)))

            self.custom_simplename = str(custom_simplename.value)

        # Load currency into a typed object
        if 'currency' in tokenless_keys:
            currency = tokenless_keys["currency"]
            if type(currency.value) != bool:
                errors.append(TokenError("currency should be a bool not a {}".format(str(type(currency.value))), Token().from_yaml_scalar_node(currency.token)))

            self.currency = bool(currency.value)

        # Load note into a typed object
        if 'note' in tokenless_keys:
            note = tokenless_keys["note"]
            if type(note.value) != str:
                errors.append(TokenError("note should be a string not a {}".format(str(type(note.value))), Token().from_yaml_scalar_node(note.token)))

            self.note = str(note.value)

        # Load recipes into a typed object
        if 'recipes' in tokenless_keys:
            for item in tokenless_keys['recipes']:
                recipe = Recipe()
                errors += recipe.parse(item)
                self.recipes.append(recipe)

        # Load custom_stack_multipliers into a typed object
        if 'custom_stack_multipliers' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["custom_stack_multipliers"]):
                errors.append(TokenError("Found Duplicate custom_stack_multipliers key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["custom_stack_multipliers"].items():
                if type(key.value) != str:
                    errors.append(TokenError("custom_stack_multipliers key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != int:
                    errors.append(TokenError("custom_stack_multipliers value should be an int not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.custom_stack_multipliers[str(key.value)] = int(value.value or 0)
        return errors

    def to_primitive(self) -> Any:
        return {
            "custom_simplename": get_primitive(self.custom_simplename),
            "currency": get_primitive(self.currency),
            "note": get_primitive(self.note),
            "recipes": get_primitive(self.recipes),
            "custom_stack_multipliers": get_primitive(self.custom_stack_multipliers),
        }

    def to_yaml(self, indent: str = "") -> str:
        output = []
        if self.custom_simplename != "":
            output.append(indent + "custom_simplename: " + yaml_string(self.custom_simplename, indent))
        if self.currency != False:
            output.append(indent + "currency: " + str(self.currency))
        if self.note != "":
            output.append(indent + "note: " + yaml_string(self.note, indent))
        if self.recipes != []:
            output.append(indent + "recipes:")
            for v in self.recipes:
                line = v.to_yaml(indent + '  ')
                line = indent + '- ' + line.removeprefix(indent + '  ')
                output.append(line)
        if self.custom_stack_multipliers != OrderedDict():
            output.append(indent + "custom_stack_multipliers:")
            for k, v in self.custom_stack_multipliers.items():
                output.append(indent + "  " + k + ": " + str(v))
        return '\n'.join(output)


# Class Generated with resource_list_type_generator.py
class Heading():
    def __init__(self) -> None:
        self.H1: str = ""
        self.H2: str = ""
        self.H3: str = ""

        self.valid_keys = ['H1', 'H2', 'H3']

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # Create error for invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found Invalid Heading key, valid Heading keys are {}".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))

        # Create error for duplicate keys
        for duplicate_key in _get_duplicate_keys(tuple_tree):
            errors.append(TokenError("Found Duplicate Heading key", Token().from_yaml_scalar_node(duplicate_key.token)))

        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}

        # Load H1 into a typed object
        if 'H1' in tokenless_keys:
            H1 = tokenless_keys["H1"]
            if type(H1.value) != str:
                errors.append(TokenError("H1 should be a string not a {}".format(str(type(H1.value))), Token().from_yaml_scalar_node(H1.token)))

            self.H1 = str(H1.value)

        # Load H2 into a typed object
        if 'H2' in tokenless_keys:
            H2 = tokenless_keys["H2"]
            if type(H2.value) != str:
                errors.append(TokenError("H2 should be a string not a {}".format(str(type(H2.value))), Token().from_yaml_scalar_node(H2.token)))

            self.H2 = str(H2.value)

        # Load H3 into a typed object
        if 'H3' in tokenless_keys:
            H3 = tokenless_keys["H3"]
            if type(H3.value) != str:
                errors.append(TokenError("H3 should be a string not a {}".format(str(type(H3.value))), Token().from_yaml_scalar_node(H3.token)))

            self.H3 = str(H3.value)
        return errors

    def to_primitive(self) -> Any:
        return {
            "H1": get_primitive(self.H1),
            "H2": get_primitive(self.H2),
            "H3": get_primitive(self.H3),
        }

    def to_yaml(self, indent: str = "") -> str:
        output = []
        if self.H1 != "":
            output.append(indent + "H1: " + yaml_string(self.H1, indent))
        if self.H2 != "":
            output.append(indent + "H2: " + yaml_string(self.H2, indent))
        if self.H3 != "":
            output.append(indent + "H3: " + yaml_string(self.H3, indent))
        return '\n'.join(output)


# Class Generated with resource_list_type_generator.py
class Recipe():
    def __init__(self) -> None:
        self.output: int = 0
        self.recipe_type: str = ""
        self.note: str = ""
        self.requirements: OrderedDict[str, int] = OrderedDict()

        self.valid_keys = ['output', 'recipe_type', 'note', 'requirements']

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # Create error for invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found Invalid Recipe key, valid Recipe keys are {}".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))

        # Create error for duplicate keys
        for duplicate_key in _get_duplicate_keys(tuple_tree):
            errors.append(TokenError("Found Duplicate Recipe key", Token().from_yaml_scalar_node(duplicate_key.token)))

        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}

        # Load output into a typed object
        if 'output' in tokenless_keys:
            output = tokenless_keys["output"]
            if type(output.value) != int:
                errors.append(TokenError("output should be an int not a {}".format(str(type(output.value))), Token().from_yaml_scalar_node(output.token)))

            self.output = int(output.value or 0)

        # Load recipe_type into a typed object
        if 'recipe_type' in tokenless_keys:
            recipe_type = tokenless_keys["recipe_type"]
            if type(recipe_type.value) != str:
                errors.append(TokenError("recipe_type should be a string not a {}".format(str(type(recipe_type.value))), Token().from_yaml_scalar_node(recipe_type.token)))

            self.recipe_type = str(recipe_type.value)

        # Load note into a typed object
        if 'note' in tokenless_keys:
            note = tokenless_keys["note"]
            if type(note.value) != str:
                errors.append(TokenError("note should be a string not a {}".format(str(type(note.value))), Token().from_yaml_scalar_node(note.token)))

            self.note = str(note.value)

        # Load requirements into a typed object
        if 'requirements' in tokenless_keys:
            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["requirements"]):
                errors.append(TokenError("Found Duplicate requirements key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["requirements"].items():
                if type(key.value) != str:
                    errors.append(TokenError("requirements key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != int:
                    errors.append(TokenError("requirements value should be an int not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.requirements[str(key.value)] = int(value.value or 0)
        return errors

    def to_primitive(self) -> Any:
        return {
            "output": get_primitive(self.output),
            "recipe_type": get_primitive(self.recipe_type),
            "note": get_primitive(self.note),
            "requirements": get_primitive(self.requirements),
        }

    def to_yaml(self, indent: str = "") -> str:
        output = []
        if self.output != 0:
            output.append(indent + "output: " + str(self.output))
        if self.recipe_type != "":
            output.append(indent + "recipe_type: " + yaml_string(self.recipe_type, indent))
        if self.note != "":
            output.append(indent + "note: " + yaml_string(self.note, indent))
        if self.requirements != OrderedDict():
            output.append(indent + "requirements:")
            for k, v in self.requirements.items():
                output.append(indent + "  " + k + ": " + str(v))
        return '\n'.join(output)
# ENDGENERATOR
