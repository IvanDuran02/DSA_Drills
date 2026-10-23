from tests.loader import load_exercise

three_sum = load_exercise("sliding_window/three_sum.py", "three_sum")

def test_three_sum():
    res = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted(res) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, 1, 1]) == []
