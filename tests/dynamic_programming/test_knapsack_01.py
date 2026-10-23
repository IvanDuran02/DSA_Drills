from tests.loader import load_exercise

knapsack_01 = load_exercise("dynamic_programming/knapsack_01.py", "knapsack_01")

def test_knapsack():
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    assert knapsack_01(weights, values, 7) == 9
