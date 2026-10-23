from tests.loader import load_exercise

merge_k_sorted_arrays = load_exercise("heaps/merge_k_sorted.py", "merge_k_sorted_arrays")

def test_merge_k():
    arrays = [[1, 4, 5], [1, 3, 4], [2, 6]]
    res = merge_k_sorted_arrays(arrays)
    assert res == [1, 1, 2, 3, 4, 4, 5, 6]
