from tests.loader import load_exercise
from drills.structures import TreeNode

is_valid_bst = load_exercise("trees/validate_bst.py", "is_valid_bst")

def test_bst():
    assert is_valid_bst(TreeNode.from_level_order([2, 1, 3])) is True
    assert is_valid_bst(TreeNode.from_level_order([5, 1, 4, None, None, 3, 6])) is False
