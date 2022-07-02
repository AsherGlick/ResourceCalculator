import heapq
from typing import TypeVar, Generic, Set, List


T = TypeVar("T")


# A sorted heap that only lets one copy of an item into it.
class UniqueHeap(Generic[T]):
    # TODO: It is possible to do this without a seperate Set but I am doing it
    # this way for implementation speed. The API for UniqueHeap will not change
    # either way so it can be swapped in-place in the future.
    _set: Set[T]
    _heap: List[T]

    def __init__(self) -> None:
        self._set = set()
        self._heap = []

    def push(self, obj: T) -> bool:
        if obj in self._set:
            return False

        self._set.add(obj)
        heapq.heappush(self._heap, obj)
        return True

    def pop(self) -> T:
        obj: T = heapq.heappop(self._heap)
        self._set.remove(obj)
        return obj

    def __len__(self) -> int:
        return len(self._heap)
