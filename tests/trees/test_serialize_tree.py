from tests.loader import load_exercise
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
