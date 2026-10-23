from typing import Optional
from reference.structures import TreeNode

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        vals = []
        def dfs(node):
            if not node:
                vals.append("#")
                return
            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)
        dfs(root)
        return ",".join(vals)

    def deserialize(self, data: str) -> Optional[TreeNode]:
        vals = data.split(",")
        idx = 0
        def dfs():
            nonlocal idx
            if idx >= len(vals) or vals[idx] == "#":
                idx += 1
                return None
            val = int(vals[idx])
            idx += 1
            node = TreeNode(val)
            node.left = dfs()
            node.right = dfs()
            return node
        return dfs()
