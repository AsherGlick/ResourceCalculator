from typing import List, Optional, Any
import yaml
from collections import OrderedDict

from .yaml_token_load import TokenBundle


################################################################################
#
################################################################################
class TokenError():
    def __init__(self, error_string: str, token: yaml.nodes.ScalarNode) -> None:
        self.error_string: str = error_string
        self.token: yaml.nodes.ScalarNode = token

    def print_error(self, raw_text: List[str]) -> None:
        start_line_number = self.token.start_mark.line
        end_line_number = self.token.end_mark.line

        start_column = self.token.start_mark.column
        end_column = self.token.end_mark.column

        print("Line \033[92m{}\033[0m: {}".format(
            str(start_line_number+1),
            self.error_string,
        ))

        print(" │{}\033[91m{}\033[0m{}".format(
            raw_text[start_line_number][0:start_column],
            raw_text[start_line_number][start_column:end_column],
            raw_text[start_line_number][end_column:],
        ))

        print(" │" + " "*(start_column) + "\033[91m"+ "^"*(end_column-start_column) + "\033[0m")


################################################################################
#
################################################################################
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

        # This is a bit of a hack to identify all the variables declared
        # previously to avoid having to keep to lists of objects in-sync
        self.valid_keys = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found invalid resource_list key, valid resource_list are " + str(self.valid_keys), invalid_key.token))

        tokenless_keys = {k.value:v  for k,v in tuple_tree.items()}

        # Load the authors field into a typed object
        if "authors" in tokenless_keys:
            for author, link in tokenless_keys["authors"].items():
                if type(author.value) != str:
                    errors.append(TokenError("Author should be a string not a " + str(type(author.value)), author.token))

                if type(link.value) != str:
                    errors.append(TokenError("Author Link should be a string not a " + str(type(link.value)), link.token))

                self.authors[str(author.value)] = str(link.value)

        # load the index page display name into a typed object
        if "index_page_display_name" in tokenless_keys:
            index_page_display_name = tokenless_keys["index_page_display_name"]
            if type(index_page_display_name.value) != str:
                errors.append(TokenError("index_page_display_name should be a string not a " + str(type(index_page_display_name.value)), index_page_display_name.token))
            self.index_page_display_name = str(index_page_display_name)
        else:
            # TOOD better tokenless errors
            print("ERROR: Missing Key index_page_display_name")

        # Load the recipe type strings into a typed object
        if "recipe_types" in tokenless_keys:
            for recipe_type, text in tokenless_keys["recipe_types"].items():
                if type(recipe_type.value) != str:
                    errors.append(TokenError("Recipe Type name should be a string not a " + str(type(recipe_type.value)), recipe_type.token))

                if type(text.value) != str:
                    errors.append(TokenError("Recipe Type instructions should be a string not a " + str(type(text.value)), text.token))

                self.recipe_types[str(recipe_type.value)] = str(text.value)
        else:
            # TODO better tokenless errors
            print("ERROR: Missing key recipe_types")


        # Load stack sizes
        if "stack_sizes" in tokenless_keys:
            for stack_name, stack_data in tokenless_keys["stack_sizes"].items():
                if type(stack_name.value) != str:
                    errors.append(TokenError("Stack Size name should be a string not a " + str(type(stack_name.value)), stack_name.token))

                stack_size = StackSize()
                errors += stack_size.parse(stack_data)

                self.stack_sizes[str(stack_name.value)] = stack_size

        if "default_stack_size" in tokenless_keys:
            default_stack_size = tokenless_keys["default_stack_size"]
            if type(default_stack_size.value) != str:
                errors.append(TokenError("default_stack_size should be a string not a " + str(type(default_stack_size.value)), default_stack_size.token))
            self.default_stack_size = str(default_stack_size)

        
        if "resources" in tokenless_keys:
            for resource_name, resource_data in tokenless_keys["resources"].items():
                if type(resource_name.value) != str:
                    errors.append(TokenError("Stack Size name should be a string not a " + str(type(resource_name.value)), resource_name.token))

                resource = Resource()
                errors += resource.parse(resource_data)

                self.resources[str(resource_name.value)] = resource

        if "game_version" in tokenless_keys:
            game_version = tokenless_keys["game_version"]
            if type(game_version.value) != str:
                errors.append(TokenError("game_version should be a string not a " + str(type(game_version.value)), game_version.token))
            self.game_version = str(game_version)


        if "banner_message" in tokenless_keys:
            banner_message = tokenless_keys["banner_message"]
            if type(banner_message.value) != str:
                errors.append(TokenError("banner_message should be a string not a " + str(type(banner_message.value)), banner_message.token))
            self.banner_message = str(banner_message)


        if "requirement_groups" in tokenless_keys:
            for requirement_group, item_list in tokenless_keys["requirement_groups"].items():
                if type(requirement_group.value) != str:
                    errors.append(TokenError("Requirement Group name should be a string not a " + str(type(requirement_group.value)), requirement_group.token))

                requirement_group_items: List[str] = []
                for item in item_list:
                    if type(item.value) != str:
                        errors.append(TokenError("Requirement Group item should be a string not a " + str(type(item.value)), item.token))

                    requirement_group_items.append(str(item.value))
                self.requirement_groups[str(requirement_group.value)] = requirement_group_items
        return errors


################################################################################
#
################################################################################
class StackSize():
    def __init__(self) -> None:
        self.quantity_multiplier: int = 0
        self.plural: str = ""
        self.extends_from: Optional[str] = None

        # This is a bit of a hack to identify all the variables declared
        # previously to avoid having to keep to lists of objects in-sync
        self.valid_keys = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]


    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found invalid resource_list key, valid resource_list are " + str(self.valid_keys), invalid_key[1]))

        tokenless_keys = {k.value:v  for k,v in tuple_tree.items()}

        if "quantity_multiplier" in tokenless_keys:
            quantity_multiplier = tokenless_keys["quantity_multiplier"]
            if type(quantity_multiplier.value) != int:
                errors.append(TokenError("quantity_multiplier should be a int not a " + str(type(quantity_multiplier.value)), quantity_multiplier.token))
            self.quantity_multiplier = int(quantity_multiplier.value)
        else:
            # TODO better tokenless errors
            print("ERROR: Missing key quantity_multiplier")

        if "plural" in tokenless_keys:
            plural = tokenless_keys["plural"]
            if type(plural.value) != str:
                errors.append(TokenError("plural should be a string not a " + str(type(plural.value)), plural.token))
            self.plural = str(plural.value)
        else:
            # TODO better tokenless errors
            print("ERROR: Missing key plural")

        if "extends_from" in tokenless_keys:
            extends_from = tokenless_keys["extends_from"]

            if extends_from.value is not None:
                if type(extends_from.value) != str:
                    errors.append(TokenError("extends_from should be a string not a " + str(type(extends_from.value)), extends_from.token))
                self.extends_from = str(extends_from.value)
        else:
            # TODO better tokenless errors
            print("ERROR: Missing key extends_from")

        return errors


################################################################################
#
################################################################################
class Resource():
    def __init__(self) -> None:
        self.recipes: List[Recipe] = []
        self.custom_stack_multipliers: OrderedDict[str, int] = OrderedDict()

        # This is a bit of a hack to identify all the variables declared
        # previously to avoid having to keep to lists of objects in-sync
        self.valid_keys = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found invalid resource_list key, valid resource_list are " + str(self.valid_keys), invalid_key[1]))

        tokenless_keys = {k.value:v  for k,v in tuple_tree.items()}

        if "recipes" in tokenless_keys:
            for recipe_data in tokenless_keys["recipes"]:
                recipe = Recipe()
                errors += recipe.parse(recipe_data)
                self.recipes.append(recipe)

        if "custom_stack_multipliers" in tokenless_keys:
            for custom_stack, stack_quantity in tokenless_keys["custom_stack_multipliers"].items():
                if type(custom_stack.value) != str:
                    errors.append(TokenError("Custom Stack name should be a string not a " + str(type(custom_stack.value)), custom_stack.token))

                if type(stack_quantity.value) != int:
                    errors.append(TokenError("Stack Quantity should be an int not a " + str(type(stack_quantity.value)), stack_quantity.token))

                self.custom_stack_multipliers[str(custom_stack.value)] = int(stack_quantity.value)

        return errors


################################################################################
#
################################################################################
class Recipe():
    def __init__(self) -> None:
        self.output: int = 0
        self.recipe_type: str = ""
        self.requirements: OrderedDict[str, int] = OrderedDict()
        self.extra_data = None # DEPRICATED FIELD

        # This is a bit of a hack to identify all the variables declared
        # previously to avoid having to keep to lists of objects in-sync
        self.valid_keys = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]

    def parse(self, tuple_tree: Any) -> List[TokenError]:
        errors: List[TokenError] = []

        # invalid keys
        for invalid_key in _get_invalid_keys(tuple_tree, self.valid_keys):
            errors.append(TokenError("Found invalid resource_list key, valid resource_list are " + str(self.valid_keys), invalid_key[1]))

        tokenless_keys = {k.value:v  for k,v in tuple_tree.items()}

        if "output" in tokenless_keys:
            output = tokenless_keys["output"]
            if type(output.value) != int:
                errors.append(TokenError("output should be an int not a " + str(type(output.value)), output.token))
            self.output = int(output.value)

        if "recipe_type" in tokenless_keys:
            recipe_type = tokenless_keys["recipe_type"]
            if type(recipe_type.value) != str:
                errors.append(TokenError("recipe_type should be a string not a " + str(type(recipe_type.value)), recipe_type.token))
            self.recipe_type = str(recipe_type.value)

        if "requirements" in tokenless_keys:
            for item, quantity in tokenless_keys["requirements"].items():
                if type(item.value) != str:
                    errors.append(TokenError("Custom Stack name should be a string not a " + str(type(item.value)), item.token))

                if type(quantity.value) != int:
                    errors.append(TokenError("Stack Quantity should be an int not a " + str(type(quantity.value)), quantity.token))

                self.requirements[str(item.value)] = int(quantity.value)


        return errors


################################################################################
#
################################################################################
def _get_invalid_keys(data: Any, valid_keys: List[str]) -> List[TokenBundle]: 
    invalid_keys: List[TokenBundle] = []

    for key in data:
        if key.value not in valid_keys:
            invalid_keys.append(key)

    return invalid_keys
