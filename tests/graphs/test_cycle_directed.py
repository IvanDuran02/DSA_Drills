from tests.loader import load_exercise

has_cycle_directed = load_exercise("graphs/cycle_directed.py", "has_cycle_directed")

def test_cycle():
    assert has_cycle_directed(3, [[0, 1], [1, 2], [2, 0]]) is True

def test_dag():
    assert has_cycle_directed(3, [[0, 1], [0, 2], [1, 2]]) is False
