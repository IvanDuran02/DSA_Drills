from tests.loader import load_exercise

count_components_dfs = load_exercise("graphs/components_dfs.py", "count_components_dfs")

def test_basic():
    assert count_components_dfs(5, [[0, 1], [1, 2], [3, 4]]) == 2

def test_isolated():
    assert count_components_dfs(4, []) == 4
