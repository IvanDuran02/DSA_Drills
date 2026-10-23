from tests.loader import load_exercise

shortest_distance_from_sources = load_exercise("graphs/multisource_bfs.py", "shortest_distance_from_sources")

def test_basic():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    d = shortest_distance_from_sources(grid)
    assert d[1][1] == 0
    assert d[0][1] == 1
    assert d[0][0] == 2
