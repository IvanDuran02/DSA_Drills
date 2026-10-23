from typing import Optional
from drills.structures import TreeNode

class Codec:
    def serialize(self, root: Optional[TreeNode]) -> str:
        raise NotImplementedError

    def deserialize(self, data: str) -> Optional[TreeNode]:
        raise NotImplementedError
