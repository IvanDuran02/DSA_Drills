from tests.loader import load_exercise

UnionFindSize = load_exercise("graphs/union_find_size.py", "UnionFindSize")

def test_size():
    uf = UnionFindSize(4)
    uf.union(0, 1)
    assert uf.get_component_size(0) == 2
    uf.union(2, 3)
    uf.union(0, 2)
    assert uf.get_component_size(3) == 4
