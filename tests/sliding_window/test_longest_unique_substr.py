from tests.loader import load_exercise

length_of_longest_substring = load_exercise("sliding_window/longest_unique_substr.py", "length_of_longest_substring")

def test_longest_substr():
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
