from tests.loader import load_exercise

fib_tab = load_exercise("dynamic_programming/fib_tab.py", "fib_tab")

def test_fib_tab():
    assert fib_tab(0) == 0
    assert fib_tab(1) == 1
    assert fib_tab(10) == 55
