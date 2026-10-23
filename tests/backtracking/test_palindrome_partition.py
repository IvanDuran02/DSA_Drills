from tests.loader import load_exercise

partition = load_exercise("backtracking/palindrome_partition.py", "partition")

def test_partition():
    res = partition("aab")
    assert sorted(res) == sorted([["a", "a", "b"], ["aa", "b"]])
