from tests.loader import load_exercise

build_min_and_max_heaps = load_exercise("heaps/heap_construction.py", "build_min_and_max_heaps")

def test_construction():
    nums = [9, 3, 7, 1, 5, 2]
    min_h, max_h = build_min_and_max_heaps(nums)
    assert min_h[0] == 1
    assert max_h[0] == 9
