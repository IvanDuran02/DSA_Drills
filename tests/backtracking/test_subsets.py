from tests.loader import load_exercise

subsets = load_exercise("backtracking/subsets.py", "subsets")

def test_subsets():
    res = subsets([1, 2, 3])
    assert len(res) == 8
    assert [] in res
    assert [1, 2, 3] in res
