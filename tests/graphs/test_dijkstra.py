from tests.loader import load_exercise

dijkstra = load_exercise("graphs/dijkstra.py", "dijkstra")

def test_dijkstra():
    edges = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]]
    res = dijkstra(4, edges, 0)
    assert res[0] == 0
    assert res[1] == 3
    assert res[2] == 1
    assert res[3] == 4
