from tests.loader import load_exercise

binary_search = load_exercise("binary_search/bs_standard.py", "binary_search")

def test_bs():
    nums = [-1, 0, 3, 5, 9, 12]
    assert binary_search(nums, 9) == 4
    assert binary_search(nums, 2) == -1
    assert binary_search([], 5) == -1
