from tests.loader import load_exercise

next_greater_elements = load_exercise("stacks/next_greater_elem.py", "next_greater_elements")

def test_next_greater():
    assert next_greater_elements([1, 2, 1]) == [2, -1, 2]
    assert next_greater_elements([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]
