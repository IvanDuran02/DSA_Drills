from typing import Optional
from reference.structures import TreeNode

def preorder_traversal(root: Optional[TreeNode]) -> list[int]:
    res = []
    def dfs(node):
        if not node:
            return
        res.append(node.val)
        dfs(node.left)
        dfs(node.right)
    dfs(root)
    return res
