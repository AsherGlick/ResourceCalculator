import unittest
from typing import Any, Optional, Union
from dataclasses import dataclass

from .action_queue import UniqueHeap


@dataclass
class Datum:
    core_data: int
    extra_data: int

    def weak_hash(self) -> int:
        return hash(self.core_data)

    def __lt__(self, other: "Datum") -> bool:
        return self.core_data < other.core_data


class TestBasicIteractions(unittest.TestCase):
    ############################################################################
    # test_basic_push_pop
    #
    # Test that we can insert multiple items into the queue and that we can
    # remove an item from the queue, removing the correct item and leaving the
    # remaining items.
    ############################################################################
    def test_basic_push_pop(self) -> None:
        unique_heap: UniqueHeap[Datum] = UniqueHeap()

        unique_heap.push(Datum(core_data=1, extra_data=1))
        unique_heap.push(Datum(core_data=2, extra_data=1))

        self.assertCountEqual(
            [x for x in unique_heap],
            [
                Datum(core_data=1, extra_data=1),
                Datum(core_data=2, extra_data=1),
            ],
        )
        self.assertEqual(len(unique_heap), 2)

        # Pop an element off the queue
        value = unique_heap.pop()
        self.assertEqual(value, Datum(core_data=1, extra_data=1))

        self.assertCountEqual(
            [x for x in unique_heap],
            [Datum(core_data=2, extra_data=1)],
        )
        self.assertEqual(len(unique_heap), 1)

    ############################################################################
    # test_weakhash_deduplication
    #
    # Test that we can insert multiple items into the queue that have the same
    # weakhash and that any new element with the same weakhash as an existing
    # element will overwrite the existing element.
    ############################################################################
    def test_weakhash_deduplication(self) -> None:
        unique_heap: UniqueHeap[Datum] = UniqueHeap()

        unique_heap.push(Datum(core_data=1, extra_data=1))
        unique_heap.push(Datum(core_data=1, extra_data=2))
        unique_heap.push(Datum(core_data=2, extra_data=1))
        unique_heap.push(Datum(core_data=2, extra_data=2))

        self.assertCountEqual(
            [x for x in unique_heap],
            [
                Datum(core_data=1, extra_data=2),
                Datum(core_data=2, extra_data=2),
            ],
        )
        self.assertEqual(len(unique_heap), 2)

        # Pop an element off the queue
        value = unique_heap.pop()
        self.assertEqual(value, Datum(core_data=1, extra_data=2))

        self.assertCountEqual(
            [x for x in unique_heap],
            [Datum(core_data=2, extra_data=2)],
        )
        self.assertEqual(len(unique_heap), 1)

    ############################################################################
    # test_delete
    #
    # Test that a weakhash can be deleted from the heap via the weakhash.
    ############################################################################
    def test_delete(self) -> None:
        unique_heap: UniqueHeap[Datum] = UniqueHeap()

        unique_heap.push(Datum(core_data=1, extra_data=1))
        unique_heap.push(Datum(core_data=2, extra_data=1))
        unique_heap.push(Datum(core_data=3, extra_data=1))
        self.assertEqual(len(unique_heap), 3)

        deleted_data = unique_heap.delete(2)
        self.assertEqual(deleted_data, Datum(core_data=2, extra_data=1))

        self.assertCountEqual(
            [x for x in unique_heap],
            [
                Datum(core_data=1, extra_data=1),
                Datum(core_data=3, extra_data=1),
            ],
        )
        self.assertEqual(len(unique_heap), 2)

    ############################################################################
    # test_delete_missing_element
    #
    # Test that if an element that does not exist in the heap is attempted to
    # be deleted then the unique heap behaves appropriately.
    ############################################################################
    def test_delete_missing_element(self) -> None:
        unique_heap: UniqueHeap[Datum] = UniqueHeap()

        unique_heap.push(Datum(core_data=1, extra_data=1))
        unique_heap.push(Datum(core_data=2, extra_data=1))
        unique_heap.push(Datum(core_data=3, extra_data=1))
        self.assertEqual(len(unique_heap), 3)

        deleted_data = unique_heap.delete(2)
        self.assertEqual(deleted_data, Datum(core_data=2, extra_data=1))
        deleted_error = unique_heap.delete(2)
        self.assertEqual(deleted_error, None)

    ############################################################################
    # test_has
    #
    # Test the check to see if a value exists inside of the heap or not.
    ############################################################################
    def test_has(self) -> None:
        unique_heap: UniqueHeap[Datum] = UniqueHeap()

        unique_heap.push(Datum(core_data=1, extra_data=1))

        self.assertEqual(unique_heap.has(1), True)
        self.assertEqual(unique_heap.has(2), False)

    ############################################################################
    # test_bad_equality
    #
    # Test that an appropriate error is raised if the generic type for the
    # UniqueHeap does not properly implement the equals operator.
    ############################################################################
    def test_bad_equality(self) -> None:
        @dataclass
        class UnequalDatum:
            core_data: int
            extra_data: int

            def weak_hash(self) -> int:
                return hash(self.core_data)

            def __lt__(self, other: "Datum") -> bool:
                return self.core_data < other.core_data

            def __eq__(self, other: Any) -> bool:
                return False

        unique_heap: UniqueHeap[UnequalDatum] = UniqueHeap()

        unique_heap.push(UnequalDatum(core_data=1, extra_data=1))
        unique_heap.push(UnequalDatum(core_data=2, extra_data=1))

        with self.assertRaises(RuntimeError):
            unique_heap.push(UnequalDatum(core_data=1, extra_data=1))

    ############################################################################
    # test_get_exists
    #
    # Test that using .get on a value that exists returns that value.
    ############################################################################
    def test_get_exists(self) -> None:
        unique_heap: UniqueHeap[Datum] = UniqueHeap()

        unique_heap.push(Datum(core_data=1, extra_data=1))

        self.assertEqual(unique_heap.get(1), Datum(core_data=1, extra_data=1))

    ############################################################################
    # test_get_doesnt_exist
    #
    # Test that using .get on a value that does not exist returns the default
    # values that are expected based on the function call.
    ############################################################################
    def test_get_doesnt_exist(self) -> None:
        unique_heap: UniqueHeap[Datum] = UniqueHeap()

        unique_heap.push(Datum(core_data=1, extra_data=1))

        default_get: Optional[Datum] = unique_heap.get(2)
        self.assertEqual(default_get, None)
        explicit_none_get: Optional[Datum] = unique_heap.get(3, None)
        self.assertEqual(explicit_none_get, None)

        fallback_datum_get: Datum = unique_heap.get(4, Datum(core_data=999, extra_data=999))
        self.assertEqual(fallback_datum_get, Datum(core_data=999, extra_data=999))

        random_other_value_get: Union[Datum, str] = unique_heap.get(5, "Not A Datum")
        self.assertEqual(random_other_value_get, "Not A Datum")
