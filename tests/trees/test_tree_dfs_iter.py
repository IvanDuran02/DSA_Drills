from tests.loader import load_exercise
from drills.structures import TreeNode

inorder_iterative = load_exercise("trees/tree_dfs_iter.py", "inorder_iterative")

def test_iter():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert inorder_iterative(root) == [1, 3, 2]
