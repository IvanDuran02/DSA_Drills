from tests.loader import load_exercise
from drills.structures import TreeNode

inorder_traversal = load_exercise("trees/inorder_rec.py", "inorder_traversal")

def test_inorder():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert inorder_traversal(root) == [1, 3, 2]
