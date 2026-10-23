import heapq

class MaxHeapPractice:
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        heapq.heappush_max(self.heap, val)

    def pop(self) -> int:
        return heapq.heappop_max(self.heap)

    def peek(self) -> int:
        return self.heap[0]
