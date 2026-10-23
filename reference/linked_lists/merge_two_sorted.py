from typing import Optional
from reference.structures import ListNode

def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    dummy = ListNode(0)
    curr = dummy
    p1, p2 = list1, list2
    while p1 and p2:
        if p1.val <= p2.val:
            curr.next = p1
            p1 = p1.next
        else:
            curr.next = p2
            p2 = p2.next
        curr = curr.next
    curr.next = p1 if p1 else p2
    return dummy.next
