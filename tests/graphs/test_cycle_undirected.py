from tests.loader import load_exercise

has_cycle_undirected = load_exercise("graphs/cycle_undirected.py", "has_cycle_undirected")

def test_cycle():
    assert has_cycle_undirected(3, [[0, 1], [1, 2], [2, 0]]) is True

def test_tree():
    assert has_cycle_undirected(4, [[0, 1], [1, 2], [2, 3]]) is False
