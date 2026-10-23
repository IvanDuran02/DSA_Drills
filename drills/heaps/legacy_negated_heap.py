import heapq

class LegacyMaxHeap:
    """
    Max-heap implemented using value negation for Python < 3.14 compatibility.
    """
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError
