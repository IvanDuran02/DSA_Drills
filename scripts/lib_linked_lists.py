"""Linked List algorithm definitions (6 exercises)"""

LINKED_LIST_EXERCISES = [
    {
        "id": "linked-list-reverse",
        "name": "Reverse Linked List",
        "category": "linked_lists",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "reverse_linked_list.py",
        "starter": '''from typing import Optional
from drills.structures import ListNode

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Reverse a singly-linked list in-place and return new head.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import ListNode

def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import ListNode

reverse_list = load_exercise("linked_lists/reverse_linked_list.py", "reverse_list")

def test_reverse():
    head = ListNode.from_list([1, 2, 3, 4, 5])
    rev = reverse_list(head)
    assert rev.to_list() == [5, 4, 3, 2, 1]
    assert reverse_list(None) is None
''',
        "hints": {
            1: "Keep 3 pointers: prev = None, curr = head, nxt = curr.next.",
            2: "Point curr.next = prev.",
            3: "Advance prev = curr and curr = nxt.",
            4: "Return prev at the end.",
            5: "See reference in reference/linked_lists/reverse_linked_list.py."
        }
    },
    {
        "id": "linked-list-merge-two",
        "name": "Merge Two Sorted Lists",
        "category": "linked_lists",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N + M)",
        "space_complexity": "O(1)",
        "file": "merge_two_sorted.py",
        "starter": '''from typing import Optional
from drills.structures import ListNode

def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
    """
    Merge two sorted linked lists into one sorted linked list.
    Target Time: O(N + M)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
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
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import ListNode

merge_two_lists = load_exercise("linked_lists/merge_two_sorted.py", "merge_two_lists")

def test_merge_two():
    l1 = ListNode.from_list([1, 2, 4])
    l2 = ListNode.from_list([1, 3, 4])
    res = merge_two_lists(l1, l2)
    assert res.to_list() == [1, 1, 2, 3, 4, 4]
''',
        "hints": {
            1: "Use dummy head node to simplify edge cases.",
            2: "Compare p1.val and p2.val, attach smaller to curr.next.",
            3: "Attach non-empty remainder: curr.next = p1 or p2.",
            4: "O(1) extra space.",
            5: "See reference in reference/linked_lists/merge_two_sorted.py."
        }
    },
    {
        "id": "linked-list-detect-cycle",
        "name": "Linked List Cycle II (Find Entry Point)",
        "category": "linked_lists",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "detect_cycle_ii.py",
        "starter": '''from typing import Optional
from drills.structures import ListNode

def detect_cycle_entry(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Return node where cycle begins, or None if no cycle.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
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
''',
        "test": '''from tests.loader import load_exercise
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
''',
        "hints": {
            1: "Find intersection point with slow and fast pointers.",
            2: "Reset p1 to head, keep p2 at intersection.",
            3: "Advance both 1 step at a time; meeting point is cycle entrance.",
            4: "Floyd's Tortoise and Hare algorithm.",
            5: "See reference in reference/linked_lists/detect_cycle_ii.py."
        }
    },
    {
        "id": "linked-list-find-middle",
        "name": "Middle of the Linked List",
        "category": "linked_lists",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 6,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "middle_node.py",
        "starter": '''from typing import Optional
from drills.structures import ListNode

def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    """
    Return middle node of linked list (second middle if two middle nodes).
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import ListNode

def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import ListNode

middle_node = load_exercise("linked_lists/middle_node.py", "middle_node")

def test_middle():
    l1 = ListNode.from_list([1, 2, 3, 4, 5])
    assert middle_node(l1).val == 3
    l2 = ListNode.from_list([1, 2, 3, 4, 5, 6])
    assert middle_node(l2).val == 4
''',
        "hints": {
            1: "Slow advances 1 step, fast advances 2 steps.",
            2: "When fast reaches end, slow is at the middle.",
            3: "O(N) time with single pass.",
            4: "O(1) space.",
            5: "See reference in reference/linked_lists/middle_node.py."
        }
    },
    {
        "id": "linked-list-remove-nth",
        "name": "Remove Nth Node From End of List",
        "category": "linked_lists",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "remove_nth_node.py",
        "starter": '''from typing import Optional
from drills.structures import ListNode

def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    """
    Remove nth node from end of list and return its head in one pass.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import ListNode

def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    fast = dummy
    slow = dummy
    for _ in range(n + 1):
        fast = fast.next
    while fast:
        slow = slow.next
        fast = fast.next
    slow.next = slow.next.next
    return dummy.next
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import ListNode

remove_nth_from_end = load_exercise("linked_lists/remove_nth_node.py", "remove_nth_from_end")

def test_remove_nth():
    l = ListNode.from_list([1, 2, 3, 4, 5])
    res = remove_nth_from_end(l, 2)
    assert res.to_list() == [1, 2, 3, 5]
    l2 = ListNode.from_list([1])
    assert remove_nth_from_end(l2, 1) is None
''',
        "hints": {
            1: "Use dummy node before head to handle removing the head node.",
            2: "Advance fast pointer n + 1 steps ahead of slow.",
            3: "Move both until fast is None; slow is right before target.",
            4: "slow.next = slow.next.next.",
            5: "See reference in reference/linked_lists/remove_nth_node.py."
        }
    },
    {
        "id": "linked-list-lru-cache",
        "name": "LRU Cache (Doubly Linked List + Hashmap)",
        "category": "linked_lists",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(1) get & put",
        "space_complexity": "O(capacity)",
        "file": "lru_cache.py",
        "starter": '''class LRUCache:
    """
    Least Recently Used (LRU) Cache supporting get and put in O(1) time.
    """
    def __init__(self, capacity: int):
        raise NotImplementedError

    def get(self, key: int) -> int:
        raise NotImplementedError

    def put(self, key: int, value: int) -> None:
        raise NotImplementedError
''',
        "reference": '''class DLinkedNode:
    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.prev = None
        self.next = None

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.head = DLinkedNode()
        self.tail = DLinkedNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: DLinkedNode):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_front(self, node: DLinkedNode):
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._remove(node)
            self._add_to_front(node)
        else:
            if len(self.cache) >= self.capacity:
                lru = self.tail.prev
                self._remove(lru)
                del self.cache[lru.key]
            new_node = DLinkedNode(key, value)
            self.cache[key] = new_node
            self._add_to_front(new_node)
''',
        "test": '''from tests.loader import load_exercise

LRUCache = load_exercise("linked_lists/lru_cache.py", "LRUCache")

def test_lru():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts 2
    assert cache.get(2) == -1
    cache.put(4, 4)  # evicts 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
''',
        "hints": {
            1: "Use doubly linked list with dummy head and tail nodes.",
            2: "Hashmap maps key -> node.",
            3: "Move accessed nodes to front of list (most recent).",
            4: "Evict node right before tail when capacity exceeded.",
            5: "See reference in reference/linked_lists/lru_cache.py."
        }
    }
]
