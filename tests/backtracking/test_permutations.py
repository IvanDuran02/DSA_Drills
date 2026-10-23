from tests.loader import load_exercise

permute = load_exercise("backtracking/permutations.py", "permute")

def test_permutations():
    res = permute([1, 2, 3])
    assert len(res) == 6
