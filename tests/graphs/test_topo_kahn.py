from tests.loader import load_exercise

topological_sort_kahn = load_exercise("graphs/topo_kahn.py", "topological_sort_kahn")

def test_kahn():
    edges = [[1, 0], [2, 0], [3, 1], [3, 2]]
    order = topological_sort_kahn(4, edges)
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        assert pos[u] < pos[v]
