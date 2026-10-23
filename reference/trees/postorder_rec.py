from typing import Optional
from reference.structures import TreeNode

def postorder_traversal(root: Optional[TreeNode]) -> list[int]:
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        dfs(node.right)
        res.append(node.val)
    dfs(root)
    return res
