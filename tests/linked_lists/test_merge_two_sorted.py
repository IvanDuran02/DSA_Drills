from tests.loader import load_exercise
from drills.structures import ListNode

merge_two_lists = load_exercise("linked_lists/merge_two_sorted.py", "merge_two_lists")

def test_merge_two():
    l1 = ListNode.from_list([1, 2, 4])
    l2 = ListNode.from_list([1, 3, 4])
    res = merge_two_lists(l1, l2)
    assert res.to_list() == [1, 1, 2, 3, 4, 4]
