from tests.loader import load_exercise

combine = load_exercise("backtracking/combinations.py", "combine")

def test_combine():
    res = combine(4, 2)
    assert len(res) == 6
