from typing import Optional
from reference.structures import TreeNode

def lowest_common_ancestor(root: Optional[TreeNode], p: int, q: int) -> Optional[TreeNode]:
    if not root or root.val == p or root.val == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right
