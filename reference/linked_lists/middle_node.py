from typing import Optional
from reference.structures import ListNode

def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
