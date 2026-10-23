from tests.loader import load_exercise

rob = load_exercise("dynamic_programming/house_robber.py", "rob")

def test_rob():
    assert rob([1, 2, 3, 1]) == 4
    assert rob([2, 7, 9, 3, 1]) == 12
