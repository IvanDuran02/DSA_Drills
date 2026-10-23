import heapq

class MedianFinder:
    def __init__(self):
        self.max_heap: list[int] = []  # lower half (Python 3.14 native max-heap)
        self.min_heap: list[int] = []  # upper half (min-heap)

    def add_num(self, num: int) -> None:
        if not self.max_heap or num <= self.max_heap[0]:
            heapq.heappush_max(self.max_heap, num)
        else:
            heapq.heappush(self.min_heap, num)

        # Balance sizes so max_heap has either same count or 1 more than min_heap
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = heapq.heappop_max(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush_max(self.max_heap, val)

    def find_median(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return float(self.max_heap[0])
        return (self.max_heap[0] + self.min_heap[0]) / 2.0
