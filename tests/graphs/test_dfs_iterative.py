from tests.loader import load_exercise

dfs_iterative = load_exercise("graphs/dfs_iterative.py", "dfs_iterative")

def test_basic_traversal():
    adj = {0: [1, 2], 1: [3], 2: [], 3: []}
    order = dfs_iterative(adj, 0)
    assert order == [0, 1, 3, 2]

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    order = dfs_iterative(adj, 0)
    assert set(order) == {0, 1, 2}
