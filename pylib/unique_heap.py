import heapq
from typing import TypeVar, Generic, Dict, List


T = TypeVar("T")


# A sorted heap that only lets one copy of an item into it.
class UniqueHeap(Generic[T]):
    # TODO: It is possible to do this without a seperate Dict but I am doing it
    # this way for implementation speed. The API for UniqueHeap will not change
    # either way so it can be swapped in-place in the future.
    _dict: Dict[int, T]
    _heap: List[T]

    def __init__(self) -> None:
        self._dict = {}
        self._heap = []

    def push(self, obj: T) -> bool:
        obj_hash = hash(obj)
        if obj_hash in self._dict:
            # Replace the object in the dict
            old_object = self._dict[obj_hash]
            self._dict[obj_hash] = obj

            # Replace the object inline in the heap
            for i, elem in enumerate(self._heap):
                if elem == old_object:
                    self._heap[i] = obj
                    return True

            raise RuntimeError("An object was inserted into the heap that does not equal itself.")

        self._dict[obj_hash] = obj
        heapq.heappush(self._heap, obj)
        return True

    def pop(self) -> T:
        obj: T = heapq.heappop(self._heap)
        del self._dict[hash(obj)]
        return obj

    def __len__(self) -> int:
        return len(self._heap)
