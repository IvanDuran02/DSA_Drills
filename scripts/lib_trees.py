"""Tree algorithm definitions (10 exercises)"""

TREE_EXERCISES = [
    {
        "id": "tree-preorder-rec",
        "name": "Recursive Preorder Traversal",
        "category": "trees",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "preorder_rec.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def preorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """
    Return preorder traversal of binary tree: Root -> Left -> Right.
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
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
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

preorder_traversal = load_exercise("trees/preorder_rec.py", "preorder_traversal")

def test_basic():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert preorder_traversal(root) == [1, 2, 3]

def test_empty():
    assert preorder_traversal(None) == []
''',
        "hints": {
            1: "Preorder visits current node before children.",
            2: "Recurse on left then right.",
            3: "Base case: if not node: return.",
            4: "Space is tree height O(H).",
            5: "See reference in reference/trees/preorder_rec.py."
        }
    },
    {
        "id": "tree-inorder-rec",
        "name": "Recursive Inorder Traversal",
        "category": "trees",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "inorder_rec.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """
    Return inorder traversal of binary tree: Left -> Root -> Right.
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import TreeNode

def inorder_traversal(root: Optional[TreeNode]) -> list[int]:
    res = []
    def dfs(node):
        if not node:
            return
        dfs(node.left)
        res.append(node.val)
        dfs(node.right)
    dfs(root)
    return res
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

inorder_traversal = load_exercise("trees/inorder_rec.py", "inorder_traversal")

def test_inorder():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert inorder_traversal(root) == [1, 3, 2]
''',
        "hints": {
            1: "Inorder produces sorted order for BSTs.",
            2: "Left, then node, then right.",
            3: "Time is O(N).",
            4: "Space is O(H).",
            5: "See reference in reference/trees/inorder_rec.py."
        }
    },
    {
        "id": "tree-postorder-rec",
        "name": "Recursive Postorder Traversal",
        "category": "trees",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "postorder_rec.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def postorder_traversal(root: Optional[TreeNode]) -> list[int]:
    """
    Return postorder traversal: Left -> Right -> Root.
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
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
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

postorder_traversal = load_exercise("trees/postorder_rec.py", "postorder_traversal")

def test_postorder():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert postorder_traversal(root) == [3, 2, 1]
''',
        "hints": {
            1: "Visit children before root.",
            2: "Useful for bottom-up tree calculations.",
            3: "O(N) time.",
            4: "O(H) space.",
            5: "See reference in reference/trees/postorder_rec.py."
        }
    },
    {
        "id": "tree-dfs-iter",
        "name": "Iterative Tree Inorder Traversal",
        "category": "trees",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "tree_dfs_iter.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def inorder_iterative(root: Optional[TreeNode]) -> list[int]:
    """
    Perform inorder traversal iteratively using an explicit stack.
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
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
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

inorder_iterative = load_exercise("trees/tree_dfs_iter.py", "inorder_iterative")

def test_iter():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert inorder_iterative(root) == [1, 3, 2]
''',
        "hints": {
            1: "Push all left children onto stack.",
            2: "Pop node, record value, then move to right child.",
            3: "Avoids stack overflow on deep trees.",
            4: "O(H) space.",
            5: "See reference in reference/trees/tree_dfs_iter.py."
        }
    },
    {
        "id": "tree-bfs-level",
        "name": "Level-Order BFS Traversal",
        "category": "trees",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "bfs_level.py",
        "starter": '''from typing import Optional
from collections import deque
from drills.structures import TreeNode

def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    """
    Return level-order traversal of nodes level by level.
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from collections import deque
from reference.structures import TreeNode

def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    if not root:
        return []
    res = []
    queue = deque([root])
    while queue:
        level_size = len(queue)
        level = []
        for _ in range(level_size):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        res.append(level)
    return res
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

level_order = load_exercise("trees/bfs_level.py", "level_order")

def test_level_order():
    root = TreeNode.from_level_order([3, 9, 20, None, None, 15, 7])
    assert level_order(root) == [[3], [9, 20], [15, 7]]
''',
        "hints": {
            1: "len(queue) at start of loop gives count of nodes on current level.",
            2: "Inner loop processes exact level_size nodes.",
            3: "Deque gives O(1) pops.",
            4: "O(N) space for bottom level.",
            5: "See reference in reference/trees/bfs_level.py."
        }
    },
    {
        "id": "tree-max-depth",
        "name": "Maximum Depth of Binary Tree",
        "category": "trees",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 6,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "max_depth.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def max_depth(root: Optional[TreeNode]) -> int:
    """
    Find maximum depth (number of nodes along longest path from root to leaf).
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import TreeNode

def max_depth(root: Optional[TreeNode]) -> int:
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

max_depth = load_exercise("trees/max_depth.py", "max_depth")

def test_max_depth():
    root = TreeNode.from_level_order([3, 9, 20, None, None, 15, 7])
    assert max_depth(root) == 3
    assert max_depth(None) == 0
''',
        "hints": {
            1: "Base case: depth of None is 0.",
            2: "1 + max(left_depth, right_depth).",
            3: "O(N) time.",
            4: "O(H) space.",
            5: "See reference in reference/trees/max_depth.py."
        }
    },
    {
        "id": "tree-validate-bst",
        "name": "Validate Binary Search Tree",
        "category": "trees",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "validate_bst.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    """
    Determine if binary tree is a valid Binary Search Tree.
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import TreeNode

def is_valid_bst(root: Optional[TreeNode]) -> bool:
    def validate(node, low, high):
        if not node:
            return True
        if not (low < node.val < high):
            return False
        return validate(node.left, low, node.val) and validate(node.right, node.val, high)
    return validate(root, float('-inf'), float('inf'))
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

is_valid_bst = load_exercise("trees/validate_bst.py", "is_valid_bst")

def test_bst():
    assert is_valid_bst(TreeNode.from_level_order([2, 1, 3])) is True
    assert is_valid_bst(TreeNode.from_level_order([5, 1, 4, None, None, 3, 6])) is False
''',
        "hints": {
            1: "Checking node.left.val < node.val is NOT sufficient; need entire range (low, high).",
            2: "Left child inherits (low, node.val).",
            3: "Right child inherits (node.val, high).",
            4: "O(N) time, O(H) space.",
            5: "See reference in reference/trees/validate_bst.py."
        }
    },
    {
        "id": "tree-lca",
        "name": "Lowest Common Ancestor (Binary Tree)",
        "category": "trees",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "lca.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def lowest_common_ancestor(root: Optional[TreeNode], p: int, q: int) -> Optional[TreeNode]:
    """
    Find Lowest Common Ancestor node containing value p and q.
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import TreeNode

def lowest_common_ancestor(root: Optional[TreeNode], p: int, q: int) -> Optional[TreeNode]:
    if not root or root.val == p or root.val == q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left if left else right
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

lowest_common_ancestor = load_exercise("trees/lca.py", "lowest_common_ancestor")

def test_lca():
    root = TreeNode.from_level_order([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    res = lowest_common_ancestor(root, 5, 1)
    assert res.val == 3
    res2 = lowest_common_ancestor(root, 5, 4)
    assert res2.val == 5
''',
        "hints": {
            1: "If root is None or matches p or q, return root.",
            2: "Recurse on left and right.",
            3: "If both left and right return non-null, root is LCA.",
            4: "Otherwise return whichever side returned non-null.",
            5: "See reference in reference/trees/lca.py."
        }
    },
    {
        "id": "tree-diameter",
        "name": "Tree Diameter",
        "category": "trees",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(N)",
        "space_complexity": "O(H)",
        "file": "diameter.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

def tree_diameter(root: Optional[TreeNode]) -> int:
    """
    Return length of longest path between any two nodes in a tree (number of edges).
    Target Time: O(N)
    Target Space: O(H)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
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
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

tree_diameter = load_exercise("trees/diameter.py", "tree_diameter")

def test_diameter():
    root = TreeNode.from_level_order([1, 2, 3, 4, 5])
    assert tree_diameter(root) == 3
''',
        "hints": {
            1: "Longest path through node is left_height + right_height.",
            2: "Helper function returns height: 1 + max(lh, rh).",
            3: "Global diameter updated at each node.",
            4: "O(N) time.",
            5: "See reference in reference/trees/diameter.py."
        }
    },
    {
        "id": "tree-serialize-deserialize",
        "name": "Serialize and Deserialize Binary Tree",
        "category": "trees",
        "difficulty": "Hard",
        "level": 3,
        "recommended_minutes": 18,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "serialize_tree.py",
        "starter": '''from typing import Optional
from drills.structures import TreeNode

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        raise NotImplementedError

    def deserialize(self, data: str) -> Optional[TreeNode]:
        raise NotImplementedError
''',
        "reference": '''from typing import Optional
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
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import TreeNode

Codec = load_exercise("trees/serialize_tree.py", "Codec")

def test_codec():
    root = TreeNode.from_level_order([1, 2, 3, None, None, 4, 5])
    codec = Codec()
    serialized = codec.serialize(root)
    deserialized = codec.deserialize(serialized)
    assert deserialized.val == 1
    assert deserialized.left.val == 2
    assert deserialized.right.left.val == 4
''',
        "hints": {
            1: "Preorder with '#' sentinel for null nodes makes unique tree reconstruction straightforward.",
            2: "Split comma-separated values and reconstruct recursively with index.",
            3: "Time O(N) serialize, O(N) deserialize.",
            4: "Space O(N).",
            5: "See reference in reference/trees/serialize_tree.py."
        }
    }
]
