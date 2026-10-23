from tests.loader import load_exercise

exist = load_exercise("backtracking/word_search.py", "exist")

def test_word_search():
    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    assert exist(board, "ABCCED") is True
    assert exist(board, "SEE") is True
    assert exist(board, "ABCB") is False
