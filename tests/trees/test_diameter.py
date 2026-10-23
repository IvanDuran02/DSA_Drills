from tests.loader import load_exercise
from drills.structures import TreeNode

tree_diameter = load_exercise("trees/diameter.py", "tree_diameter")

def test_diameter():
    root = TreeNode.from_level_order([1, 2, 3, 4, 5])
    assert tree_diameter(root) == 3
