from tests.loader import load_exercise

unique_paths = load_exercise("dynamic_programming/unique_paths.py", "unique_paths")

def test_paths():
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
