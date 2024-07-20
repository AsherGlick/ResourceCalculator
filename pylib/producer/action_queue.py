import heapq
from typing import TypeVar, Generic, Dict, List, Protocol, Optional, Iterator


class WeakHash(Protocol):
    def weak_hash(self) -> int:
        ...


T = TypeVar("T", bound=WeakHash)


################################################################################
# UniqueHeap
#
# A heap, or priority queue, that deduplicates objects based on their
# .weak_hash() function. Any new objects inserted into the heap that have the
# same hash as existing types will replace the existing types.
################################################################################
class UniqueHeap(Generic[T]):
    _dict: Dict[int, T]
    _heap: List[T]

    ############################################################################
    # __init__
    #
    # Initialize the UniqueHeap with starter values for the member variables.
    # As of python 3.10 we cannot do this in the class declaration because it
    # will instantiate a single dict or list for all instances of UniqueHeap.
    ############################################################################
    def __init__(self) -> None:
        self._dict = {}
        self._heap = []

    ############################################################################
    # push
    #
    # Pushes a new item into the heap. If the item's weak_hash is the same as
    # an object that already exists then the existing object is replaced. If
    # an object replaced then the old object is returned.
    ############################################################################
    def push(self, obj: T) -> Optional[T]:
        obj_hash = obj.weak_hash()
        if obj_hash in self._dict:
            # Replace the object in the dict
            old_object = self._dict[obj_hash]
            self._dict[obj_hash] = obj

            # Replace the object inline in the heap
            for i, elem in enumerate(self._heap):
                if elem == old_object:
                    self._heap[i] = obj
                    return old_object

            raise RuntimeError("An object was inserted into the heap that does not equal itself.")

        self._dict[obj_hash] = obj
        heapq.heappush(self._heap, obj)
        return None

    ############################################################################
    # pop
    #
    # Removes the top element of the heap and returns it.
    ############################################################################
    def pop(self) -> T:
        obj: T = heapq.heappop(self._heap)
        del self._dict[obj.weak_hash()]
        return obj

    ############################################################################
    # has
    #
    # Returns if the UniqueHeap has an element with a matching weak hash.
    ############################################################################
    def has(self, weak_hash: int) -> bool:
        return weak_hash in self._dict

    ############################################################################
    # get
    #
    # Returns a value from within the unique heap, or None if the heap does
    # not contain that data.
    # TODO: We should probably replicate other .get() functions and allow for
    #   a default value to be passed in, to return instead of None.
    ############################################################################
    def get(self, weak_hash: int) -> Optional[T]:
        return self._dict.get(weak_hash, None)

    ############################################################################
    # delete
    #
    # Removes an element from the unique heap.
    # TODO: This is kinda slow, it is not clear yet if that is a problem so we
    #   will leave this as-is. However we might change it with something else
    #   in the future, like nulling out the field, skipping over null fields,
    #   keeping track of the number of nulled fields for __len__, and taking
    #   all that into account when adding a new element that replaces a null
    #   field in the heap.
    ############################################################################
    def delete(self, weak_hash: int) -> Optional[T]:
        obj = self._dict.get(weak_hash, None)

        if obj is None:
            return None

        del self._dict[weak_hash]

        self._heap.remove(obj)
        heapq.heapify(self._heap)

        return obj

    ############################################################################
    # __len__
    #
    # Returns the length of the heap.
    ############################################################################
    def __len__(self) -> int:
        return len(self._heap)

    def __iter__(self) -> Iterator[T]:
        return self._heap.__iter__()
