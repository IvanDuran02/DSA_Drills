from tests.loader import load_exercise
from drills.structures import ListNode

detect_cycle_entry = load_exercise("linked_lists/detect_cycle_ii.py", "detect_cycle_entry")

def test_entry():
    n1 = ListNode(3)
    n2 = ListNode(2)
    n3 = ListNode(0)
    n4 = ListNode(-4)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n2
    assert detect_cycle_entry(n1) == n2
    assert detect_cycle_entry(ListNode(1)) is None
