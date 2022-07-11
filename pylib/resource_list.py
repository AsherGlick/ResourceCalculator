from typing import List, Optional, Any
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
        return OrderedDict([(k, get_primitive(v)) for k, v in obj.items()])
    elif hasattr(obj, "to_primitive"):
        return obj.to_primitive()
    else:
        return obj


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
        self.recipe_types: OrderedDict[str, str] = OrderedDict()
        self.stack_sizes: OrderedDict[str, StackSize] = OrderedDict()
        self.default_stack_size: str = ""
        self.resources: OrderedDict[str, Resource] = OrderedDict()
        self.game_version: str = ""
        self.banner_message: str = ""
        self.requirement_groups: OrderedDict[str, List[str]] = OrderedDict()
        self.row_group_count: int = 1

        self.valid_keys = ['authors', 'index_page_display_name', 'recipe_types', 'stack_sizes', 'default_stack_size', 'resources', 'game_version', 'banner_message', 'requirement_groups', 'row_group_count']

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
                errors.append(TokenError("Found Duplicate Author key", Token().from_yaml_scalar_node(duplicate_key.token)))

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

        # Load recipe_types into a typed object
        if 'recipe_types' in tokenless_keys:

            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["recipe_types"]):
                errors.append(TokenError("Found Duplicate RecipeType key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["recipe_types"].items():
                if type(key.value) != str:
                    errors.append(TokenError("recipe_types key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != str:
                    errors.append(TokenError("recipe_types value should be a string not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.recipe_types[str(key.value)] = str(value.value)

        # Load stack_sizes into a typed object
        if 'stack_sizes' in tokenless_keys:

            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["stack_sizes"]):
                errors.append(TokenError("Found Duplicate Stack Sizes key", Token().from_yaml_scalar_node(duplicate_key.token)))

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
                errors.append(TokenError("Found Duplicate Resources key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["resources"].items():
                if type(key.value) != str:
                    errors.append(TokenError("resources key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                Resource_subobject = Resource()
                errors += Resource_subobject.parse(value)

                self.resources[str(key.value)] = Resource_subobject

        # Load game_version into a typed object
        if 'game_version' in tokenless_keys:
            game_version = tokenless_keys["game_version"]
            if type(game_version.value) != str:
                errors.append(TokenError("game_version should be a string not a {}".format(str(type(game_version.value))), Token().from_yaml_scalar_node(game_version.token)))

            self.game_version = str(game_version.value)

        # Load banner_message into a typed object
        if 'banner_message' in tokenless_keys:
            banner_message = tokenless_keys["banner_message"]
            if type(banner_message.value) != str:
                errors.append(TokenError("banner_message should be a string not a {}".format(str(type(banner_message.value))), Token().from_yaml_scalar_node(banner_message.token)))

            self.banner_message = str(banner_message.value)

        # Load requirement_groups into a typed object
        if 'requirement_groups' in tokenless_keys:

            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["requirement_groups"]):
                errors.append(TokenError("Found Duplicate RequirementGroup key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["requirement_groups"].items():
                if type(key.value) != str:
                    errors.append(TokenError("requirement_groups key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                item_list: List[str] = []
                for item in value:
                    if type(item.value) != str:
                        errors.append(TokenError("requirement_groups element should be a string not a {}".format(str(type(item.value))), Token().from_yaml_scalar_node(item.token)))
                    item_list.append(str(item.value))
                self.requirement_groups[str(key.value)] = item_list

        # Load row_group_count into a typed object
        if 'row_group_count' in tokenless_keys:
            row_group_count = tokenless_keys["row_group_count"]
            if type(row_group_count.value) != int:
                errors.append(TokenError("row_group_count should be an int not a {}".format(str(type(row_group_count.value))), Token().from_yaml_scalar_node(row_group_count.token)))

            self.row_group_count = int(row_group_count.value)
        return errors

    def to_primitive(self) -> Any:
        return {
            "authors": get_primitive(self.authors),
            "index_page_display_name": get_primitive(self.index_page_display_name),
            "recipe_types": get_primitive(self.recipe_types),
            "stack_sizes": get_primitive(self.stack_sizes),
            "default_stack_size": get_primitive(self.default_stack_size),
            "resources": get_primitive(self.resources),
            "game_version": get_primitive(self.game_version),
            "banner_message": get_primitive(self.banner_message),
            "requirement_groups": get_primitive(self.requirement_groups),
            "row_group_count": get_primitive(self.row_group_count),
        }


# Class Generated with resource_list_type_generator.py
class StackSize():
    def __init__(self) -> None:
        self.quantity_multiplier: int = 0
        self.plural: str = ""
        self.extends_from: Optional[str] = None
        self.custom_multipliers: OrderedDict[str, int] = OrderedDict()

        self.valid_keys = ['quantity_multiplier', 'plural', 'extends_from', 'custom_multipliers']

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

            self.quantity_multiplier = int(quantity_multiplier.value)

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
            for duplicate_key in _get_duplicate_keys(tokenless_keys['custom_multipliers']):
                errors.append(TokenError("Found Duplicate CustomMultipliers key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["custom_multipliers"].items():
                if type(key.value) != str:
                    errors.append(TokenError("custom_multipliers key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != int:
                    errors.append(TokenError("custom_multipliers value should be an int not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.custom_multipliers[str(key.value)] = int(value.value)
        return errors

    def to_primitive(self) -> Any:
        return {
            "quantity_multiplier": get_primitive(self.quantity_multiplier),
            "plural": get_primitive(self.plural),
            "extends_from": get_primitive(self.extends_from),
            "custom_multipliers": get_primitive(self.custom_multipliers),
        }


# Class Generated with resource_list_type_generator.py
class Resource():
    def __init__(self) -> None:
        self.recipes: List[Recipe] = []
        self.custom_stack_multipliers: OrderedDict[str, int] = OrderedDict()
        self.custom_simplename: str = ""
        self.currency: bool = False

        self.valid_keys = ['recipes', 'custom_stack_multipliers', 'custom_simplename', 'currency']

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # Create error for invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found Invalid Resource key, valid Resource keys are {}".format(str(self.valid_keys)), Token().from_yaml_scalar_node(invalid_key.token)))

        # Create error for duplicate keys
        for duplicate_key in _get_duplicate_keys(tuple_tree):
            errors.append(TokenError("Found Duplicate Resource key", Token().from_yaml_scalar_node(duplicate_key.token)))

        tokenless_keys = {k.value: v for k, v in tuple_tree.items()}

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
                errors.append(TokenError("Found Duplicate Custom Stack Multiplier key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["custom_stack_multipliers"].items():
                if type(key.value) != str:
                    errors.append(TokenError("custom_stack_multipliers key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != int:
                    errors.append(TokenError("custom_stack_multipliers value should be an int not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.custom_stack_multipliers[str(key.value)] = int(value.value)

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
        return errors

    def to_primitive(self) -> Any:
        return {
            "recipes": get_primitive(self.recipes),
            "custom_stack_multipliers": get_primitive(self.custom_stack_multipliers),
            "custom_simplename": get_primitive(self.custom_simplename),
            "currency": get_primitive(self.currency),
        }


# Class Generated with resource_list_type_generator.py
class Recipe():
    def __init__(self) -> None:
        self.output: int = 0
        self.recipe_type: str = ""
        self.requirements: OrderedDict[str, int] = OrderedDict()

        self.valid_keys = ['output', 'recipe_type', 'requirements']

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

            self.output = int(output.value)

        # Load recipe_type into a typed object
        if 'recipe_type' in tokenless_keys:
            recipe_type = tokenless_keys["recipe_type"]
            if type(recipe_type.value) != str:
                errors.append(TokenError("recipe_type should be a string not a {}".format(str(type(recipe_type.value))), Token().from_yaml_scalar_node(recipe_type.token)))

            self.recipe_type = str(recipe_type.value)

        # Load requirements into a typed object
        if 'requirements' in tokenless_keys:

            # Create error for duplicate keys
            for duplicate_key in _get_duplicate_keys(tokenless_keys["requirements"]):
                errors.append(TokenError("Found Duplicate Requirements key", Token().from_yaml_scalar_node(duplicate_key.token)))

            for key, value in tokenless_keys["requirements"].items():
                if type(key.value) != str:
                    errors.append(TokenError("requirements key should be a string not a {}".format(str(type(key.value))), Token().from_yaml_scalar_node(key.token)))

                if type(value.value) != int:
                    errors.append(TokenError("requirements value should be an int not a {}".format(str(type(value.value))), Token().from_yaml_scalar_node(value.token)))

                self.requirements[str(key.value)] = int(value.value)
        return errors

    def to_primitive(self) -> Any:
        return {
            "output": get_primitive(self.output),
            "recipe_type": get_primitive(self.recipe_type),
            "requirements": get_primitive(self.requirements),
        }

    def to_yaml(self) -> str:
        lines: List[str] = []
        lines.append("    - output: " + str(self.output))
        lines.append("      recipe_type: " + str(self.recipe_type))
        lines.append("      requirements:")
        for requirement, value in self.requirements.items():
            lines.append("        " + requirement + ": " + str(value))
        return "\n".join(lines)

# ENDGENERATOR
