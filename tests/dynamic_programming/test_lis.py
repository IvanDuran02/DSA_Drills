from tests.loader import load_exercise

length_of_lis = load_exercise("dynamic_programming/lis.py", "length_of_lis")

def test_lis():
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7]) == 1
