import heapq

class MinHeapPractice:
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError
