from tests.loader import load_exercise
import heapq

replace_min_and_max = load_exercise("heaps/heap_replace.py", "replace_min_and_max")

def test_replacement():
    min_h = [1, 3, 5]
    max_h = [10, 8, 6]
    heapq.heapify(min_h)
    heapq.heapify_max(max_h)
    p_min, p_max = replace_min_and_max(min_h, max_h, 7)
    assert p_min == 1
    assert p_max == 10
    assert min_h[0] == 3
    assert max_h[0] == 8
