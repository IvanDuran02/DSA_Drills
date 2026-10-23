from tests.loader import load_exercise

dfs_recursive = load_exercise("graphs/dfs_recursive.py", "dfs_recursive")

def test_basic_traversal():
    adj = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    order = dfs_recursive(adj, 0)
    assert order[0] == 0
    assert set(order) == {0, 1, 2, 3}

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    order = dfs_recursive(adj, 0)
    assert order == [0, 1, 2]
