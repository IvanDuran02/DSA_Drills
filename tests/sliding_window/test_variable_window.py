from tests.loader import load_exercise

min_sub_array_len = load_exercise("sliding_window/variable_window.py", "min_sub_array_len")

def test_var_window():
    assert min_sub_array_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert min_sub_array_len(4, [1, 4, 4]) == 1
    assert min_sub_array_len(11, [1, 1, 1, 1, 1]) == 0
