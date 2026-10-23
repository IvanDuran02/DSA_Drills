class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        self.parent[root_x] = root_y
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
