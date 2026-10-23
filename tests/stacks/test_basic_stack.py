from tests.loader import load_exercise
import pytest

ArrayStack = load_exercise("stacks/basic_stack.py", "ArrayStack")

def test_stack_ops():
    s = ArrayStack()
    assert s.is_empty() is True
    s.push(10)
    s.push(20)
    assert s.peek() == 20
    assert s.pop() == 20
    assert s.pop() == 10
    assert s.is_empty() is True
