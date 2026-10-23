class UnionFindSize:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.size = [1] * size
        self.num_components = size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.size[root_x] < self.size[root_y]:
            root_x, root_y = root_y, root_x
        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]
        self.num_components -= 1
        return True

    def get_component_size(self, x: int) -> int:
        return self.size[self.find(x)]
