import heapq

class LegacyMaxHeap:
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        heapq.heappush(self.heap, -val)

    def pop(self) -> int:
        return -heapq.heappop(self.heap)

    def peek(self) -> int:
        return -self.heap[0]
