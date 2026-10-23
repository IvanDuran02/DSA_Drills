from tests.loader import load_exercise

longest_common_subsequence = load_exercise("dynamic_programming/lcs.py", "longest_common_subsequence")

def test_lcs():
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "def") == 0
