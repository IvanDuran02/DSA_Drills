from tests.loader import load_exercise

bfs = load_exercise("graphs/bfs.py", "bfs")

def test_basic_bfs():
    adj = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}
    order = bfs(adj, 0)
    assert order == [0, 1, 2, 3, 4]

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    assert bfs(adj, 0) == [0, 1, 2]
