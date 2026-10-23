from __future__ import annotations
from typing import Any, Optional


class ListNode:
    def __init__(self, val: int = 0, next: Optional[ListNode] = None):
        self.val = val
        self.next = next

    @classmethod
    def from_list(cls, values: list[int]) -> Optional[ListNode]:
        dummy = ListNode(0)
        curr = dummy
        for v in values:
            curr.next = ListNode(v)
            curr = curr.next
        return dummy.next

    def to_list(self) -> list[int]:
        res = []
        curr = self
        visited = set()
        while curr:
            if id(curr) in visited:
                break  # cycle protection
            visited.add(id(curr))
            res.append(curr.val)
            curr = curr.next
        return res

    def __repr__(self) -> str:
        return f"ListNode({self.to_list()})"


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional[TreeNode] = None,
        right: Optional[TreeNode] = None
    ):
        self.val = val
        self.left = left
        self.right = right

    @classmethod
    def from_level_order(cls, values: list[Optional[int]]) -> Optional[TreeNode]:
        if not values or values[0] is None:
            return None
        root = TreeNode(values[0])
        queue = [root]
        i = 1
        n = len(values)
        while queue and i < n:
            node = queue.pop(0)
            if i < n and values[i] is not None:
                node.left = TreeNode(values[i])
                queue.append(node.left)
            i += 1
            if i < n and values[i] is not None:
                node.right = TreeNode(values[i])
                queue.append(node.right)
            i += 1
        return root

    def to_level_order(self) -> list[Optional[int]]:
        res = []
        queue = [self]
        while queue:
            node = queue.pop(0)
            if node:
                res.append(node.val)
                queue.append(node.left)
                queue.append(node.right)
            else:
                res.append(None)
        while res and res[-1] is None:
            res.pop()
        return res

    def __repr__(self) -> str:
        return f"TreeNode({self.to_level_order()})"
