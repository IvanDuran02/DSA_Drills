from tests.loader import load_exercise

build_adj_list = load_exercise("graphs/adj_list.py", "build_adj_list")

def test_basic_undirected():
    edges = [[0, 1], [1, 2]]
    adj = build_adj_list(3, edges, directed=False)
    assert set(adj[0]) == {1}
    assert set(adj[1]) == {0, 2}
    assert set(adj[2]) == {1}

def test_basic_directed():
    edges = [[0, 1], [1, 2]]
    adj = build_adj_list(3, edges, directed=True)
    assert adj[0] == [1]
    assert adj[1] == [2]
    assert adj[2] == []

def test_edge_empty():
    adj = build_adj_list(2, [], directed=False)
    assert adj == {0: [], 1: []}
