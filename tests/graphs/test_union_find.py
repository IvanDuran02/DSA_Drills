from tests.loader import load_exercise

UnionFind = load_exercise("graphs/union_find.py", "UnionFind")

def test_uf():
    uf = UnionFind(5)
    assert not uf.connected(0, 1)
    assert uf.union(0, 1) is True
    assert uf.connected(0, 1) is True
    assert uf.union(0, 1) is False
