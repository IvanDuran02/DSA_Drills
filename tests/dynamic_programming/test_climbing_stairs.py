from tests.loader import load_exercise

climb_stairs = load_exercise("dynamic_programming/climbing_stairs.py", "climb_stairs")

def test_stairs():
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
