from tests.loader import load_exercise

previous_smaller_element = load_exercise("stacks/monotonic_stack.py", "previous_smaller_element")

def test_prev_smaller():
    assert previous_smaller_element([4, 5, 2, 10, 8]) == [-1, 4, -1, 2, 2]
