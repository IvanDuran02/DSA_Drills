from tests.loader import load_exercise

count_components_bfs = load_exercise("graphs/components_bfs.py", "count_components_bfs")

def test_basic():
    assert count_components_bfs(5, [[0, 1], [1, 2], [3, 4]]) == 2

def test_empty():
    assert count_components_bfs(3, []) == 3
