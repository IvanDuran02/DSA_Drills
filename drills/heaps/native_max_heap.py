import heapq

class MaxHeapPractice:
    """
    Max-heap using Python 3.14 native heapq max-heap functions:
    heapq.heappush_max, heapq.heappop_max
    """
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError
