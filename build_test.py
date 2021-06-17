import build
from typing import Dict, Tuple, List, Set, OrderedDict
from pylib.yaml_token_load import ordered_load
from pylib.resource_list import ResourceList, Resource, StackSize, Recipe, TokenError, Token, get_primitive

import unittest




def test_load(input_yaml: str) -> List[TokenError]:
    errors: List[TokenError] = []
    with open(input_yaml, 'r', encoding="utf_8") as f:
        yaml_data = ordered_load(f)
        resource_list = ResourceList()
        errors += resource_list.parse(yaml_data)

    resources: OrderedDict[str, Resource] = resource_list.resources
    resources = build.expand_raw_resource(resources)

    recipe_types: OrderedDict[str, str] = resource_list.recipe_types

    stack_sizes: OrderedDict[str, StackSize] = resource_list.stack_sizes

    errors += build.lint_resources("TEST CALCULATOR", resources, recipe_types, stack_sizes)

    return errors

class Test_Invalid_Yaml(unittest.TestCase):
    def setUp(self) -> None:
        pass

    ############################################################################
    #
    ############################################################################
    def test_invalid_resource_list_key(self) -> None:
        errors = test_load("tests/good_fields.yaml")
        desired_errors: List[TokenError] = []
        self.assertListEqual(errors, desired_errors)

    ############################################################################
    #
    ############################################################################
    def test_invalid_raw_resource_error(self) -> None:
        errors = test_load("tests/invalid_raw_resource.yaml")
        desired_errors: List[TokenError] = [
            TokenError('MyResource has an invalid "Raw Resource"', Token(0, 0, 0, 0)),
            TokenError('MyResource must have a "Raw Resource" which outputs 1 and has a requirement of 0 of itself', Token(0, 0, 0, 0))
        ]
        self.assertListEqual(errors, desired_errors)

    ############################################################################
    #
    ############################################################################
    def test_missing_raw_resource_error(self) -> None:
        errors = test_load("tests/missing_raw_resource.yaml")
        desired_errors: List[TokenError] = [
            TokenError('MyResource must have a "Raw Resource" which outputs 1 and has a requirement of 0 of itself', Token(0, 0, 0, 0))
        ]
        self.assertListEqual(errors, desired_errors)

    ############################################################################
    #
    ############################################################################
    def test_invalid_resource_list_key_error(self) -> None:
        errors = test_load("tests/invalid_resource_list_key.yaml")
        desired_errors: List[TokenError] = [
            TokenError(
                "Found Invalid ResourceList key, valid ResourceList keys are ['authors', 'index_page_display_name', 'recipe_types', 'stack_sizes', 'default_stack_size', 'resources', 'game_version', 'banner_message', 'requirement_groups', 'row_group_count']",
                Token(10, 10, 0, 16)
            )
        ]
        self.assertListEqual(errors, desired_errors)

    ############################################################################
    # Test that an error is thrown when the key or value of the
    # resource_list.authors field is not a string
    ############################################################################
    def test_non_string_authors_error(self) -> None:
        errors = test_load("tests/non_string_authors.yaml")
        desired_errors: List[TokenError] = [
            TokenError("authors key should be a string not a <class 'int'>", Token(2, 2, 2, 4)),
            TokenError("authors value should be a string not a <class 'int'>", Token(2, 2, 6, 12))
        ]
        self.assertListEqual(errors, desired_errors)

    ############################################################################
    #
    ############################################################################
    def test_non_string_index_display_name(self) -> None:
        errors = test_load("tests/non_string_index_display_name.yaml")
        desired_errors: List[TokenError] = [
            TokenError("index_page_display_name should be a string not a <class 'int'>", Token(5, 5, 25, 27))
        ]
        self.assertListEqual(errors, desired_errors)

    ############################################################################
    #
    ############################################################################
    def test_non_string_recipe_types(self) -> None:
        errors = test_load("tests/non_string_recipe_types.yaml")
        desired_errors: List[TokenError] = [
            TokenError("recipe_types key should be a string not a <class 'int'>", Token(9, 9, 2, 6)),
            TokenError("recipe_types value should be a string not a <class 'int'>", Token(9, 9, 8, 13)),
            TokenError('Unused recipe_type "-999"', Token(0, 0, 0, 0))
        ]
        self.assertListEqual(errors, desired_errors)
