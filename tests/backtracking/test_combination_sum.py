from tests.loader import load_exercise

combination_sum = load_exercise("backtracking/combination_sum.py", "combination_sum")

def test_comb_sum():
    res = combination_sum([2, 3, 6, 7], 7)
    assert [7] in res
    assert [2, 2, 3] in res
