from tests.loader import load_exercise

is_bipartite = load_exercise("graphs/bipartite.py", "is_bipartite")

def test_bipartite():
    assert is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True
    assert is_bipartite([[1, 2], [0, 2], [0, 1]]) is False
