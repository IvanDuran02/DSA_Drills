from tests.loader import load_exercise

num_islands_dfs = load_exercise("graphs/grid_dfs.py", "num_islands_dfs")

def test_islands():
    grid = [["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]
    assert num_islands_dfs(grid) == 2
