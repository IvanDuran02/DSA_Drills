from tests.loader import load_exercise
from drills.structures import ListNode

reverse_list = load_exercise("linked_lists/reverse_linked_list.py", "reverse_list")

def test_reverse():
    head = ListNode.from_list([1, 2, 3, 4, 5])
    rev = reverse_list(head)
    assert rev.to_list() == [5, 4, 3, 2, 1]
    assert reverse_list(None) is None
