from tests.loader import load_exercise

topological_sort_dfs = load_exercise("graphs/topo_dfs.py", "topological_sort_dfs")

def test_dag():
    edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
    order = topological_sort_dfs(4, edges)
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        assert pos[u] < pos[v]

def test_cycle():
    assert topological_sort_dfs(2, [[0, 1], [1, 0]]) == []
