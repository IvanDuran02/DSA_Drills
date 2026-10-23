from tests.loader import load_exercise

MinStack = load_exercise("stacks/min_stack.py", "MinStack")

def test_min_stack():
    s = MinStack()
    s.push(-2)
    s.push(0)
    s.push(-3)
    assert s.get_min() == -3
    s.pop()
    assert s.top() == 0
    assert s.get_min() == -2
