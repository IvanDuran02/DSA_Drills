from tests.loader import load_exercise

fib_memo = load_exercise("dynamic_programming/fib_memo.py", "fib_memo")

def test_fib_memo():
    assert fib_memo(0) == 0
    assert fib_memo(1) == 1
    assert fib_memo(10) == 55
