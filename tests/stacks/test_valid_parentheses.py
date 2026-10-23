from tests.loader import load_exercise

is_valid = load_exercise("stacks/valid_parentheses.py", "is_valid")

def test_valid_parens():
    assert is_valid("()") is True
    assert is_valid("()[]{}") is True
    assert is_valid("(]") is False
    assert is_valid("([)]") is False
