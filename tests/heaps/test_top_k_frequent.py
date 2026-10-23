from tests.loader import load_exercise

top_k_frequent = load_exercise("heaps/top_k_frequent.py", "top_k_frequent")

def test_top_k():
    res = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    assert set(res) == {1, 2}
