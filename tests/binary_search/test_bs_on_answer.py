from tests.loader import load_exercise

min_eating_speed = load_exercise("binary_search/bs_on_answer.py", "min_eating_speed")

def test_koko():
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
