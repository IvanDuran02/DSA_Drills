from tests.loader import load_exercise
from drills.structures import TreeNode

postorder_traversal = load_exercise("trees/postorder_rec.py", "postorder_traversal")

def test_postorder():
    root = TreeNode.from_level_order([1, None, 2, 3])
    assert postorder_traversal(root) == [3, 2, 1]
