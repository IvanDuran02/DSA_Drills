from typing import Optional
from reference.structures import TreeNode

def inorder_iterative(root: Optional[TreeNode]) -> list[int]:
    res = []
    stack = []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        res.append(curr.val)
        curr = curr.right
    return res
