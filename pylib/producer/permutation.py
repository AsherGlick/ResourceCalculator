from typing import Generator, List, TypeVar, Dict

T = TypeVar("T")
K = TypeVar("K")


################################################################################
# permutations
#
# Get all possible permutations of values given a list of possible options for
# each value.
################################################################################
def permutations(elements: List[List[T]]) -> Generator[List[T], None, None]:
    for element in elements:
        if len(element) == 0:
            raise ValueError("Cannot get permutations when one of the options has no values")

    # The current index of each element's possible values
    indexes: List[int] = [0] * len(elements)

    # Indicator of the next element to increment. Used only in the following loop
    increment_index: int = 0
    while(True):
        yield [elements[i][x] for i, x in enumerate(indexes)]

        while True:
            indexes[increment_index] += 1

            if indexes[increment_index] >= len(elements[increment_index]):
                indexes[increment_index] = 0
                increment_index += 1

                if increment_index >= len(indexes):
                    return
            else:
                increment_index = 0
                break


################################################################################
# dict_permutations
#
# A utility function to allow calling the permutations function on a dict where
# each value of the dict has a list of possible values.
################################################################################
def dict_permutations(elements: Dict[K, List[T]]) -> Generator[Dict[K, T], None, None]:
    for element_name, element in elements.items():
        if len(element) == 0:
            raise ValueError("Cannot get permutations when one of the options has no values. {} is an array of length 0.".format(element_name))

    listified_items: List[List[T]] = []
    dict_items_index: List[K] = []

    for element_name, element in elements.items():
        dict_items_index.append(element_name)
        listified_items.append(element)

    generator = permutations(listified_items)

    for permutation in generator:
        yield {i[0]: i[1] for i in zip(dict_items_index, permutation)}
