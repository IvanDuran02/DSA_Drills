from tests.loader import load_exercise
from drills.structures import TreeNode

max_depth = load_exercise("trees/max_depth.py", "max_depth")

def test_max_depth():
    root = TreeNode.from_level_order([3, 9, 20, None, None, 15, 7])
    assert max_depth(root) == 3
    assert max_depth(None) == 0
