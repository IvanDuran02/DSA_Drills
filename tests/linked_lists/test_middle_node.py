from tests.loader import load_exercise
from drills.structures import ListNode

middle_node = load_exercise("linked_lists/middle_node.py", "middle_node")

def test_middle():
    l1 = ListNode.from_list([1, 2, 3, 4, 5])
    assert middle_node(l1).val == 3
    l2 = ListNode.from_list([1, 2, 3, 4, 5, 6])
    assert middle_node(l2).val == 4
