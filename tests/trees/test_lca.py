from tests.loader import load_exercise
from drills.structures import TreeNode

lowest_common_ancestor = load_exercise("trees/lca.py", "lowest_common_ancestor")

def test_lca():
    root = TreeNode.from_level_order([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    res = lowest_common_ancestor(root, 5, 1)
    assert res.val == 3
    res2 = lowest_common_ancestor(root, 5, 4)
    assert res2.val == 5
