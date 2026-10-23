from typing import Optional
from reference.structures import ListNode

def detect_cycle_entry(head: Optional[ListNode]) -> Optional[ListNode]:
    if not head or not head.next:
        return None
    slow = head
    fast = head
    has_cycle = False
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            has_cycle = True
            break
    if not has_cycle:
        return None
    p1 = head
    p2 = slow
    while p1 != p2:
        p1 = p1.next
        p2 = p2.next
    return p1
