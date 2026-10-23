"""Graph algorithm definitions (17 exercises)"""

GRAPH_EXERCISES = [
    {
        "id": "graph-adj-list",
        "name": "Build an Adjacency List",
        "category": "graphs",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "file": "adj_list.py",
        "starter": '''def build_adj_list(n: int, edges: list[list[int]], directed: bool = False) -> dict[int, list[int]]:
    """
    Build an adjacency list representation from an edge list for vertices 0 to n-1.
    Target Time: O(V + E)
    Target Space: O(V + E)
    """
    raise NotImplementedError
''',
        "reference": '''def build_adj_list(n: int, edges: list[list[int]], directed: bool = False) -> dict[int, list[int]]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
    return adj
''',
        "test": '''from tests.loader import load_exercise

build_adj_list = load_exercise("graphs/adj_list.py", "build_adj_list")

def test_basic_undirected():
    edges = [[0, 1], [1, 2]]
    adj = build_adj_list(3, edges, directed=False)
    assert set(adj[0]) == {1}
    assert set(adj[1]) == {0, 2}
    assert set(adj[2]) == {1}

def test_basic_directed():
    edges = [[0, 1], [1, 2]]
    adj = build_adj_list(3, edges, directed=True)
    assert adj[0] == [1]
    assert adj[1] == [2]
    assert adj[2] == []

def test_edge_empty():
    adj = build_adj_list(2, [], directed=False)
    assert adj == {0: [], 1: []}
''',
        "hints": {
            1: "Test with disconnected vertices and check dict initialization.",
            2: "Initialize a list for each vertex from 0 to n-1 before adding edges.",
            3: "Remember to add reverse edges (v -> u) only when directed is False.",
            4: "Adjacency lists use O(V) space for dictionary keys and O(E) for neighbors.",
            5: "See reference implementation in reference/graphs/adj_list.py."
        }
    },
    {
        "id": "graph-dfs-rec",
        "name": "Recursive DFS Traversal",
        "category": "graphs",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "dfs_recursive.py",
        "starter": '''def dfs_recursive(adj: dict[int, list[int]], start: int) -> list[int]:
    """
    Perform recursive Depth First Search traversal starting from vertex 'start'.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''def dfs_recursive(adj: dict[int, list[int]], start: int) -> list[int]:
    visited = set()
    order = []

    def dfs(node: int):
        visited.add(node)
        order.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)

    if start in adj:
        dfs(start)
    return order
''',
        "test": '''from tests.loader import load_exercise

dfs_recursive = load_exercise("graphs/dfs_recursive.py", "dfs_recursive")

def test_basic_traversal():
    adj = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    order = dfs_recursive(adj, 0)
    assert order[0] == 0
    assert set(order) == {0, 1, 2, 3}

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    order = dfs_recursive(adj, 0)
    assert order == [0, 1, 2]
''',
        "hints": {
            1: "Ensure visited set prevents infinite recursion on cycles.",
            2: "Helper function dfs(u) should add u to visited, append to order, then recurse.",
            3: "Call dfs(start) only if start exists in graph.",
            4: "Recursive call stack consumes O(V) auxiliary space in the worst case.",
            5: "See reference implementation in reference/graphs/dfs_recursive.py."
        }
    },
    {
        "id": "graph-dfs-iter",
        "name": "Iterative DFS Traversal",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "dfs_iterative.py",
        "starter": '''def dfs_iterative(adj: dict[int, list[int]], start: int) -> list[int]:
    """
    Perform iterative Depth First Search using an explicit stack.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''def dfs_iterative(adj: dict[int, list[int]], start: int) -> list[int]:
    if start not in adj:
        return []
    visited = set()
    stack = [start]
    order = []
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            order.append(node)
            for neighbor in reversed(adj.get(node, [])):
                if neighbor not in visited:
                    stack.append(neighbor)
    return order
''',
        "test": '''from tests.loader import load_exercise

dfs_iterative = load_exercise("graphs/dfs_iterative.py", "dfs_iterative")

def test_basic_traversal():
    adj = {0: [1, 2], 1: [3], 2: [], 3: []}
    order = dfs_iterative(adj, 0)
    assert order == [0, 1, 3, 2]

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    order = dfs_iterative(adj, 0)
    assert set(order) == {0, 1, 2}
''',
        "hints": {
            1: "Mark nodes visited when popping from stack, not when pushing.",
            2: "Reverse neighbor order when pushing to visit left-to-right.",
            3: "An explicit stack avoids Python recursion limits.",
            4: "Time is O(V + E) since each vertex is processed once.",
            5: "See reference implementation in reference/graphs/dfs_iterative.py."
        }
    },
    {
        "id": "graph-bfs",
        "name": "Breadth First Search (BFS)",
        "category": "graphs",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "bfs.py",
        "starter": '''from collections import deque

def bfs(adj: dict[int, list[int]], start: int) -> list[int]:
    """
    Traverse graph using Breadth First Search starting from 'start'.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''from collections import deque

def bfs(adj: dict[int, list[int]], start: int) -> list[int]:
    if start not in adj:
        return []
    visited = {start}
    queue = deque([start])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return order
''',
        "test": '''from tests.loader import load_exercise

bfs = load_exercise("graphs/bfs.py", "bfs")

def test_basic_bfs():
    adj = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}
    order = bfs(adj, 0)
    assert order == [0, 1, 2, 3, 4]

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    assert bfs(adj, 0) == [0, 1, 2]
''',
        "hints": {
            1: "Use collections.deque for O(1) pops.",
            2: "Mark visited upon enqueueing.",
            3: "BFS explores level by level.",
            4: "Queue size is bounded by O(V).",
            5: "See reference implementation in reference/graphs/bfs.py."
        }
    },
    {
        "id": "graph-components-dfs",
        "name": "Connected Components using DFS",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "components_dfs.py",
        "starter": '''def count_components_dfs(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components in an undirected graph with n nodes (0 to n-1) using DFS.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''def count_components_dfs(n: int, edges: list[list[int]]) -> int:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()
    components = 0

    def dfs(node: int):
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                dfs(neighbor)

    for i in range(n):
        if i not in visited:
            components += 1
            dfs(i)

    return components
''',
        "test": '''from tests.loader import load_exercise

count_components_dfs = load_exercise("graphs/components_dfs.py", "count_components_dfs")

def test_basic():
    assert count_components_dfs(5, [[0, 1], [1, 2], [3, 4]]) == 2

def test_isolated():
    assert count_components_dfs(4, []) == 4
''',
        "hints": {
            1: "Outer loop checks every vertex 0..n-1.",
            2: "Trigger DFS if unvisited and increment count.",
            3: "Undirected edges need bidirectional insertion.",
            4: "Visited set spans all components.",
            5: "See reference in reference/graphs/components_dfs.py."
        }
    },
    {
        "id": "graph-components-bfs",
        "name": "Connected Components using BFS",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "components_bfs.py",
        "starter": '''def count_components_bfs(n: int, edges: list[list[int]]) -> int:
    """
    Count connected components in an undirected graph with n nodes using BFS.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''from collections import deque

def count_components_bfs(n: int, edges: list[list[int]]) -> int:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()
    components = 0

    for i in range(n):
        if i not in visited:
            components += 1
            visited.add(i)
            queue = deque([i])
            while queue:
                curr = queue.popleft()
                for neighbor in adj[curr]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)

    return components
''',
        "test": '''from tests.loader import load_exercise

count_components_bfs = load_exercise("graphs/components_bfs.py", "count_components_bfs")

def test_basic():
    assert count_components_bfs(5, [[0, 1], [1, 2], [3, 4]]) == 2

def test_empty():
    assert count_components_bfs(3, []) == 3
''',
        "hints": {
            1: "BFS queue drains each component completely.",
            2: "Increment count on new queue launch.",
            3: "Mark visited when enqueueing.",
            4: "Complexity is O(V + E).",
            5: "See reference in reference/graphs/components_bfs.py."
        }
    },
    {
        "id": "graph-cycle-undirected",
        "name": "Undirected Cycle Detection",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "cycle_undirected.py",
        "starter": '''def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    """
    Determine whether an undirected graph contains a cycle.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    visited = set()

    def dfs(node: int, parent: int) -> bool:
        visited.add(node)
        for neighbor in adj[node]:
            if neighbor not in visited:
                if dfs(neighbor, node):
                    return True
            elif neighbor != parent:
                return True
        return False

    for i in range(n):
        if i not in visited:
            if dfs(i, -1):
                return True

    return False
''',
        "test": '''from tests.loader import load_exercise

has_cycle_undirected = load_exercise("graphs/cycle_undirected.py", "has_cycle_undirected")

def test_cycle():
    assert has_cycle_undirected(3, [[0, 1], [1, 2], [2, 0]]) is True

def test_tree():
    assert has_cycle_undirected(4, [[0, 1], [1, 2], [2, 3]]) is False
''',
        "hints": {
            1: "Track parent to avoid false cycle from bidirectional edge.",
            2: "If neighbor in visited and neighbor != parent, cycle found.",
            3: "Loop 0..n-1 to handle disconnected components.",
            4: "Time complexity O(V + E).",
            5: "See reference in reference/graphs/cycle_undirected.py."
        }
    },
    {
        "id": "graph-cycle-directed",
        "name": "Directed Cycle Detection",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "cycle_directed.py",
        "starter": '''def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    """
    Determine whether a directed graph contains a cycle.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)

    state = [0] * n  # 0=unvisited, 1=in current recursion stack, 2=finished

    def dfs(node: int) -> bool:
        state[node] = 1
        for neighbor in adj[node]:
            if state[neighbor] == 1:
                return True
            if state[neighbor] == 0:
                if dfs(neighbor):
                    return True
        state[node] = 2
        return False

    for i in range(n):
        if state[i] == 0:
            if dfs(i):
                return True

    return False
''',
        "test": '''from tests.loader import load_exercise

has_cycle_directed = load_exercise("graphs/cycle_directed.py", "has_cycle_directed")

def test_cycle():
    assert has_cycle_directed(3, [[0, 1], [1, 2], [2, 0]]) is True

def test_dag():
    assert has_cycle_directed(3, [[0, 1], [0, 2], [1, 2]]) is False
''',
        "hints": {
            1: "3-state coloring: unvisited (0), visiting (1), finished (2).",
            2: "Back edge to state 1 signifies cycle.",
            3: "Set state back to 2 upon leaving recursion.",
            4: "O(V + E) time.",
            5: "See reference in reference/graphs/cycle_directed.py."
        }
    },
    {
        "id": "graph-topo-dfs",
        "name": "Topological Sort using DFS",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "topo_dfs.py",
        "starter": '''def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:
    """
    Return a valid topological order of nodes 0 to n-1. Return empty list if cycle exists.
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)

    state = [0] * n
    order = []
    has_cycle = False

    def dfs(node: int):
        nonlocal has_cycle
        if has_cycle:
            return
        state[node] = 1
        for neighbor in adj[node]:
            if state[neighbor] == 1:
                has_cycle = True
                return
            if state[neighbor] == 0:
                dfs(neighbor)
        state[node] = 2
        order.append(node)

    for i in range(n):
        if state[i] == 0:
            dfs(i)
            if has_cycle:
                return []

    return order[::-1]
''',
        "test": '''from tests.loader import load_exercise

topological_sort_dfs = load_exercise("graphs/topo_dfs.py", "topological_sort_dfs")

def test_dag():
    edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
    order = topological_sort_dfs(4, edges)
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        assert pos[u] < pos[v]

def test_cycle():
    assert topological_sort_dfs(2, [[0, 1], [1, 0]]) == []
''',
        "hints": {
            1: "Postorder completion DFS reversed gives topological sort.",
            2: "Use cycle detection with state 1 to catch cycles.",
            3: "Return [] if cycle is detected.",
            4: "Complexity is O(V + E).",
            5: "See reference in reference/graphs/topo_dfs.py."
        }
    },
    {
        "id": "graph-topo-kahn",
        "name": "Topological Sort using Kahn's Algorithm",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "topo_kahn.py",
        "starter": '''from collections import deque

def topological_sort_kahn(n: int, edges: list[list[int]]) -> list[int]:
    """
    Return a valid topological order using Kahn's algorithm (in-degree BFS).
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''from collections import deque

def topological_sort_kahn(n: int, edges: list[list[int]]) -> list[int]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    in_degree = [0] * n
    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([i for i in range(n) if in_degree[i] == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order if len(order) == n else []
''',
        "test": '''from tests.loader import load_exercise

topological_sort_kahn = load_exercise("graphs/topo_kahn.py", "topological_sort_kahn")

def test_kahn():
    edges = [[1, 0], [2, 0], [3, 1], [3, 2]]
    order = topological_sort_kahn(4, edges)
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        assert pos[u] < pos[v]
''',
        "hints": {
            1: "Compute in-degrees. Enqueue all 0-in-degree vertices.",
            2: "Decrement neighbor in-degree on pop; enqueue when 0.",
            3: "If result length < n, cycle exists.",
            4: "O(V + E) time.",
            5: "See reference in reference/graphs/topo_kahn.py."
        }
    },
    {
        "id": "graph-union-find",
        "name": "Union-Find with Path Compression",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(alpha(N))",
        "space_complexity": "O(N)",
        "file": "union_find.py",
        "starter": '''class UnionFind:
    def __init__(self, size: int):
        raise NotImplementedError

    def find(self, x: int) -> int:
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def connected(self, x: int, y: int) -> bool:
        raise NotImplementedError
''',
        "reference": '''class UnionFind:
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
''',
        "test": '''from tests.loader import load_exercise

UnionFind = load_exercise("graphs/union_find.py", "UnionFind")

def test_uf():
    uf = UnionFind(5)
    assert not uf.connected(0, 1)
    assert uf.union(0, 1) is True
    assert uf.connected(0, 1) is True
    assert uf.union(0, 1) is False
''',
        "hints": {
            1: "Path compression: self.parent[x] = self.find(self.parent[x]).",
            2: "Union connects root of x to root of y.",
            3: "Returns False if roots are equal.",
            4: "Nearly O(1) amortized.",
            5: "See reference in reference/graphs/union_find.py."
        }
    },
    {
        "id": "graph-union-find-size",
        "name": "Union-Find with Union by Size/Rank",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(alpha(N))",
        "space_complexity": "O(N)",
        "file": "union_find_size.py",
        "starter": '''class UnionFindSize:
    def __init__(self, size: int):
        raise NotImplementedError

    def find(self, x: int) -> int:
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def get_component_size(self, x: int) -> int:
        raise NotImplementedError
''',
        "reference": '''class UnionFindSize:
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
''',
        "test": '''from tests.loader import load_exercise

UnionFindSize = load_exercise("graphs/union_find_size.py", "UnionFindSize")

def test_size():
    uf = UnionFindSize(4)
    uf.union(0, 1)
    assert uf.get_component_size(0) == 2
    uf.union(2, 3)
    uf.union(0, 2)
    assert uf.get_component_size(3) == 4
''',
        "hints": {
            1: "Attach smaller tree to larger tree.",
            2: "Update root size by adding smaller size.",
            3: "Decrement num_components.",
            4: "O(alpha(N)) optimal bounds.",
            5: "See reference in reference/graphs/union_find_size.py."
        }
    },
    {
        "id": "graph-multisource-bfs",
        "name": "Multi-Source BFS",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(R * C)",
        "space_complexity": "O(R * C)",
        "file": "multisource_bfs.py",
        "starter": '''def shortest_distance_from_sources(grid: list[list[int]]) -> list[list[int]]:
    """
    Find shortest Manhattan distance from any 1 to every cell in binary grid.
    Target Time: O(R * C)
    Target Space: O(R * C)
    """
    raise NotImplementedError
''',
        "reference": '''from collections import deque

def shortest_distance_from_sources(grid: list[list[int]]) -> list[list[int]]:
    if not grid or not grid[0]:
        return []
    rows, cols = len(grid), len(grid[0])
    dist = [[-1] * cols for _ in range(rows)]
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                dist[r][c] = 0
                queue.append((r, c))

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))

    return dist
''',
        "test": '''from tests.loader import load_exercise

shortest_distance_from_sources = load_exercise("graphs/multisource_bfs.py", "shortest_distance_from_sources")

def test_basic():
    grid = [[0, 0, 0], [0, 1, 0], [0, 0, 0]]
    d = shortest_distance_from_sources(grid)
    assert d[1][1] == 0
    assert d[0][1] == 1
    assert d[0][0] == 2
''',
        "hints": {
            1: "Enqueue all sources with value 1 at time 0.",
            2: "dist matrix initialized with -1 marks unvisited.",
            3: "Expand 4-directionally level by level.",
            4: "Complexity is O(R * C).",
            5: "See reference in reference/graphs/multisource_bfs.py."
        }
    },
    {
        "id": "graph-grid-dfs",
        "name": "Grid DFS (Number of Islands)",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(R * C)",
        "space_complexity": "O(R * C)",
        "file": "grid_dfs.py",
        "starter": '''def num_islands_dfs(grid: list[list[str]]) -> int:
    """
    Count connected components of '1's in 2D grid using DFS.
    Target Time: O(R * C)
    Target Space: O(R * C)
    """
    raise NotImplementedError
''',
        "reference": '''def num_islands_dfs(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    islands = 0

    def dfs(r: int, c: int):
        visited.add((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "1" and (nr, nc) not in visited:
                dfs(nr, nc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and (r, c) not in visited:
                islands += 1
                dfs(r, c)

    return islands
''',
        "test": '''from tests.loader import load_exercise

num_islands_dfs = load_exercise("graphs/grid_dfs.py", "num_islands_dfs")

def test_islands():
    grid = [["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]]
    assert num_islands_dfs(grid) == 2
''',
        "hints": {
            1: "Sink or mark visited connected land cells.",
            2: "Check bounds 0 <= nr < R and 0 <= nc < C.",
            3: "Count increments once per unvisited '1' found.",
            4: "O(R * C) time.",
            5: "See reference in reference/graphs/grid_dfs.py."
        }
    },
    {
        "id": "graph-grid-bfs",
        "name": "Grid BFS (Shortest Path)",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(R * C)",
        "space_complexity": "O(R * C)",
        "file": "grid_bfs.py",
        "starter": '''def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    """
    Shortest 8-directional clear path from (0,0) to (n-1, n-1) with value 0.
    Target Time: O(R * C)
    Target Space: O(R * C)
    """
    raise NotImplementedError
''',
        "reference": '''from collections import deque

def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    if not grid or grid[0][0] != 0 or grid[-1][-1] != 0:
        return -1
    n = len(grid)
    if n == 1:
        return 1

    queue = deque([(0, 0, 1)])
    visited = {(0, 0)}

    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    while queue:
        r, c, length = queue.popleft()
        if r == n - 1 and c == n - 1:
            return length
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append((nr, nc, length + 1))

    return -1
''',
        "test": '''from tests.loader import load_exercise

shortest_path_binary_matrix = load_exercise("graphs/grid_bfs.py", "shortest_path_binary_matrix")

def test_path():
    grid = [[0, 1], [1, 0]]
    assert shortest_path_binary_matrix(grid) == 2
''',
        "hints": {
            1: "Check if start or end is blocked (value 1).",
            2: "Use 8 directions.",
            3: "First arrival at (n-1, n-1) is guaranteed shortest.",
            4: "O(R * C) time.",
            5: "See reference in reference/graphs/grid_bfs.py."
        }
    },
    {
        "id": "graph-dijkstra",
        "name": "Dijkstra's Algorithm",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "file": "dijkstra.py",
        "starter": '''def dijkstra(n: int, edges: list[list[int]], start: int) -> dict[int, int]:
    """
    Dijkstra shortest path algorithm. edges = [[u, v, weight], ...].
    Target Time: O((V + E) log V)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''import heapq

def dijkstra(n: int, edges: list[list[int]], start: int) -> dict[int, int]:
    adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))

    distances = {i: -1 for i in range(n)}
    pq = [(0, start)]

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if distances[u] != -1:
            continue
        distances[u] = curr_dist
        for v, weight in adj[u]:
            if distances[v] == -1:
                heapq.heappush(pq, (curr_dist + weight, v))

    return distances
''',
        "test": '''from tests.loader import load_exercise

dijkstra = load_exercise("graphs/dijkstra.py", "dijkstra")

def test_dijkstra():
    edges = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]]
    res = dijkstra(4, edges, 0)
    assert res[0] == 0
    assert res[1] == 3
    assert res[2] == 1
    assert res[3] == 4
''',
        "hints": {
            1: "Min-heap of (distance_so_far, node).",
            2: "Skip if distances[u] != -1.",
            3: "Greedy choice property applies.",
            4: "O((V + E) log V).",
            5: "See reference in reference/graphs/dijkstra.py."
        }
    },
    {
        "id": "graph-bipartite",
        "name": "Bipartite Graph Detection",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "file": "bipartite.py",
        "starter": '''def is_bipartite(graph: list[list[int]]) -> bool:
    """
    Determine if an undirected graph is bipartite (2-colorable).
    Target Time: O(V + E)
    Target Space: O(V)
    """
    raise NotImplementedError
''',
        "reference": '''def is_bipartite(graph: list[list[int]]) -> bool:
    n = len(graph)
    color = {}

    for i in range(n):
        if i not in color:
            color[i] = 0
            stack = [i]
            while stack:
                u = stack.pop()
                for v in graph[u]:
                    if v not in color:
                        color[v] = 1 - color[u]
                        stack.append(v)
                    elif color[v] == color[u]:
                        return False
    return True
''',
        "test": '''from tests.loader import load_exercise

is_bipartite = load_exercise("graphs/bipartite.py", "is_bipartite")

def test_bipartite():
    assert is_bipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True
    assert is_bipartite([[1, 2], [0, 2], [0, 1]]) is False
''',
        "hints": {
            1: "Try 2-coloring with 0 and 1.",
            2: "If adjacent has same color, not bipartite.",
            3: "Handle disconnected components.",
            4: "O(V + E) time.",
            5: "See reference in reference/graphs/bipartite.py."
        }
    }
]
