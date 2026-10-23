from tests.loader import load_exercise
from drills.structures import ListNode

has_cycle = load_exercise("sliding_window/fast_slow_pointers.py", "has_cycle")

def test_cycle():
    n1 = ListNode(3)
    n2 = ListNode(2)
    n3 = ListNode(0)
    n4 = ListNode(-4)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n2  # cycle back to n2
    assert has_cycle(n1) is True
    assert has_cycle(ListNode(1)) is False
