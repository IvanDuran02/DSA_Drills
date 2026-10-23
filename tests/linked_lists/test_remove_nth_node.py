from tests.loader import load_exercise
from drills.structures import ListNode

remove_nth_from_end = load_exercise("linked_lists/remove_nth_node.py", "remove_nth_from_end")

def test_remove_nth():
    l = ListNode.from_list([1, 2, 3, 4, 5])
    res = remove_nth_from_end(l, 2)
    assert res.to_list() == [1, 2, 3, 5]
    l2 = ListNode.from_list([1])
    assert remove_nth_from_end(l2, 1) is None
