from typing import Optional
from reference.structures import ListNode

def has_cycle(head: Optional[ListNode]) -> bool:
    if not head or not head.next:
        return False
    slow = head
    fast = head.next
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    return False
