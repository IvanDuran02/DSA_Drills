from tests.loader import load_exercise

subsets_with_dup = load_exercise("backtracking/subsets_duplicates.py", "subsets_with_dup")

def test_subsets_dup():
    res = subsets_with_dup([1, 2, 2])
    assert len(res) == 6
