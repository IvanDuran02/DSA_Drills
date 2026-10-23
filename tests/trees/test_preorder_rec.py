from tests.loader import load_exercise
from drills.structures import TreeNode

preorder_traversal = load_exercise("trees/preorder_rec.py", "preorder_traversal")

def test_basic():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert preorder_traversal(root) == [1, 2, 3]

def test_empty():
    assert preorder_traversal(None) == []
