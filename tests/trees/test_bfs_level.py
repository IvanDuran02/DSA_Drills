from tests.loader import load_exercise
from drills.structures import TreeNode

level_order = load_exercise("trees/bfs_level.py", "level_order")

def test_level_order():
    root = TreeNode.from_level_order([3, 9, 20, None, None, 15, 7])
    assert level_order(root) == [[3], [9, 20], [15, 7]]
