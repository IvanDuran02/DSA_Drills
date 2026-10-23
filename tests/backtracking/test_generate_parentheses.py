from tests.loader import load_exercise

generate_parenthesis = load_exercise("backtracking/generate_parentheses.py", "generate_parenthesis")

def test_gen_parens():
    res = generate_parenthesis(3)
    assert len(res) == 5
    assert "((()))" in res
    assert "()()()" in res
