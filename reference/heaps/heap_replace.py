import heapq

def replace_min_and_max(min_heap: list[int], max_heap: list[int], val: int) -> tuple[int, int]:
    popped_min = heapq.heapreplace(min_heap, val)
    popped_max = heapq.heapreplace_max(max_heap, val)
    return popped_min, popped_max
