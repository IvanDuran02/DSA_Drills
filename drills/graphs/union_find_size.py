class UnionFindSize:
    def __init__(self, size: int):
        raise NotImplementedError

    def find(self, x: int) -> int:
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def get_component_size(self, x: int) -> int:
        raise NotImplementedError
