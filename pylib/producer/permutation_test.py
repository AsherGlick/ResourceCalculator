from typing import Dict, List
import unittest

from .permutation import dict_permutations, permutations


class Test_Basic_Permutations(unittest.TestCase):
    # maxDiff = 999999

    def test_two_by_two(self) -> None:
        values: List[List[int]] = [
            [1, 2],
            [3, 4],
        ]
        self.assertCountEqual(
            [x for x in permutations(values)],
            [
                [1, 3],
                [1, 4],
                [2, 3],
                [2, 4],
            ]
        )

    def test_three_by_three(self) -> None:
        values: List[List[int]] = [
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9],
        ]

        self.assertCountEqual(
            [x for x in permutations(values)],
            [
                [1, 4, 7], [1, 4, 8], [1, 4, 9],
                [1, 5, 7], [1, 5, 8], [1, 5, 9],
                [1, 6, 7], [1, 6, 8], [1, 6, 9],

                [2, 4, 7], [2, 4, 8], [2, 4, 9],
                [2, 5, 7], [2, 5, 8], [2, 5, 9],
                [2, 6, 7], [2, 6, 8], [2, 6, 9],

                [3, 4, 7], [3, 4, 8], [3, 4, 9],
                [3, 5, 7], [3, 5, 8], [3, 5, 9],
                [3, 6, 7], [3, 6, 8], [3, 6, 9],
            ]
        )

    def test_error_on_empty_option(self) -> None:
        values: List[List[int]] = [
            [1, 2],
            [],
            [3, 4],
        ]
        with self.assertRaises(ValueError):
            [x for x in permutations(values)]

    def test_increasing_choices(self) -> None:
        values: List[List[int]] = [
            [1],
            [2, 3],
            [4, 5, 6],
        ]

        self.assertCountEqual(
            [x for x in permutations(values)],
            [
                [1, 2, 4],
                [1, 2, 5],
                [1, 2, 6],

                [1, 3, 4],
                [1, 3, 5],
                [1, 3, 6],
            ]
        )

    def test_decreasing_choices(self) -> None:
        values: List[List[int]] = [
            [1, 2, 3],
            [4, 5],
            [6],
        ]

        self.assertCountEqual(
            [x for x in permutations(values)],
            [
                [1, 4, 6],
                [1, 5, 6],

                [2, 4, 6],
                [2, 5, 6],

                [3, 4, 6],
                [3, 5, 6],
            ]
        )

    def test_dictionary_conversion(self) -> None:
        values: Dict[str, List[int]] = {
            "a": [1, 2, 3],
            "b": [4, 5, 6],
        }
        self.assertCountEqual(
            [x for x in dict_permutations(values)],
            [
                {"a": 1, "b": 4},
                {"a": 1, "b": 5},
                {"a": 1, "b": 6},

                {"a": 2, "b": 4},
                {"a": 2, "b": 5},
                {"a": 2, "b": 6},

                {"a": 3, "b": 4},
                {"a": 3, "b": 5},
                {"a": 3, "b": 6},
            ]
        )

    def test_error_on_empty_dictionary_option(self) -> None:
        values: Dict[str, List[int]] = {
            "a": [1, 2],
            "b": [],
            "c": [3, 4],
        }
        with self.assertRaises(ValueError):
            [x for x in dict_permutations(values)]
