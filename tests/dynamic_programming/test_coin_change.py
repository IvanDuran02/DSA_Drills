from tests.loader import load_exercise

coin_change = load_exercise("dynamic_programming/coin_change.py", "coin_change")

def test_coin_change():
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
