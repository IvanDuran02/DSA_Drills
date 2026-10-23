from tests.loader import load_exercise

shortest_path_binary_matrix = load_exercise("graphs/grid_bfs.py", "shortest_path_binary_matrix")

def test_path():
    grid = [[0, 1], [1, 0]]
    assert shortest_path_binary_matrix(grid) == 2
