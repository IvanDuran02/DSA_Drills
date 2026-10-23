import heapq

def build_min_and_max_heaps(nums: list[int]) -> tuple[list[int], list[int]]:
    min_h = list(nums)
    max_h = list(nums)
    heapq.heapify(min_h)
    heapq.heapify_max(max_h)
    return min_h, max_h
