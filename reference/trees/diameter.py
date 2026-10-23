from typing import Optional
from reference.structures import TreeNode

def tree_diameter(root: Optional[TreeNode]) -> int:
    diameter = 0
    def height(node):
        nonlocal diameter
        if not node:
            return 0
        lh = height(node.left)
        rh = height(node.right)
        diameter = max(diameter, lh + rh)
        return 1 + max(lh, rh)
    height(root)
    return diameter
