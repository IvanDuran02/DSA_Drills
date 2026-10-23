#!/usr/bin/env python3
"""
Exercise generator for Algorithm Drills.
Generates all 88 algorithm drills across 9 categories with:
- YAML metadata (exercises/metadata/)
- Student starter implementations with raise NotImplementedError (drills/)
- Full working reference implementations (reference/)
- Pytest suites with basic, edge, and stress tests (tests/)
"""

import os
import yaml
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

EXERCISES = [
    # GRAPHS (17)
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
        "func": "build_adj_list",
        "signature": "def build_adj_list(n: int, edges: list[list[int]], directed: bool = False) -> dict[int, list[int]]:",
        "doc": "Build an adjacency list representation from an edge list for vertices 0 to n-1.",
        "starter": """def build_adj_list(n: int, edges: list[list[int]], directed: bool = False) -> dict[int, list[int]]:
    \"\"\"
    Build an adjacency list representation from an edge list for vertices 0 to n-1.
    Target Time: O(V + E)
    Target Space: O(V + E)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def build_adj_list(n: int, edges: list[list[int]], directed: bool = False) -> dict[int, list[int]]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
    return adj
""",
        "test": """from tests.loader import load_exercise
import pytest

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

def test_stress_disconnected():
    adj = build_adj_list(5, [[0, 1]], directed=False)
    assert len(adj) == 5
    assert adj[4] == []
""",
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
        "func": "dfs_recursive",
        "signature": "def dfs_recursive(adj: dict[int, list[int]], start: int) -> list[int]:",
        "doc": "Perform recursive Depth First Search starting from vertex 'start' and return traversal order.",
        "starter": """def dfs_recursive(adj: dict[int, list[int]], start: int) -> list[int]:
    \"\"\"
    Perform recursive Depth First Search traversal starting from vertex 'start'.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def dfs_recursive(adj: dict[int, list[int]], start: int) -> list[int]:
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
""",
        "test": """from tests.loader import load_exercise
import pytest

dfs_recursive = load_exercise("graphs/dfs_recursive.py", "dfs_recursive")

def test_basic_traversal():
    adj = {0: [1, 2], 1: [0, 3], 2: [0], 3: [1]}
    order = dfs_recursive(adj, 0)
    assert order[0] == 0
    assert set(order) == {0, 1, 2, 3}
    assert len(order) == 4

def test_edge_single_node():
    adj = {0: []}
    assert dfs_recursive(adj, 0) == [0]

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    order = dfs_recursive(adj, 0)
    assert order == [0, 1, 2]

def test_stress_disconnected():
    adj = {0: [1], 1: [0], 2: [3], 3: [2]}
    order = dfs_recursive(adj, 0)
    assert set(order) == {0, 1}
""",
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
        "func": "dfs_iterative",
        "signature": "def dfs_iterative(adj: dict[int, list[int]], start: int) -> list[int]:",
        "doc": "Perform iterative Depth First Search using an explicit stack.",
        "starter": """def dfs_iterative(adj: dict[int, list[int]], start: int) -> list[int]:
    \"\"\"
    Perform iterative Depth First Search using an explicit stack.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def dfs_iterative(adj: dict[int, list[int]], start: int) -> list[int]:
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
""",
        "test": """from tests.loader import load_exercise
import pytest

dfs_iterative = load_exercise("graphs/dfs_iterative.py", "dfs_iterative")

def test_basic_traversal():
    adj = {0: [1, 2], 1: [3], 2: [], 3: []}
    order = dfs_iterative(adj, 0)
    assert order == [0, 1, 3, 2]

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    order = dfs_iterative(adj, 0)
    assert set(order) == {0, 1, 2}
    assert len(order) == 3

def test_edge_empty():
    assert dfs_iterative({}, 0) == []
""",
        "hints": {
            1: "Mark nodes visited when popping from stack, not when pushing.",
            2: "Reverse the neighbor order when pushing to process in natural left-to-right order.",
            3: "An explicit stack avoids Python recursion depth limits.",
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
        "func": "bfs",
        "signature": "def bfs(adj: dict[int, list[int]], start: int) -> list[int]:",
        "doc": "Traverse graph in level-order using collections.deque.",
        "starter": """from collections import deque

def bfs(adj: dict[int, list[int]], start: int) -> list[int]:
    \"\"\"
    Traverse graph using Breadth First Search starting from 'start'.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """from collections import deque

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
""",
        "test": """from tests.loader import load_exercise
from collections import deque
import pytest

bfs = load_exercise("graphs/bfs.py", "bfs")

def test_basic_bfs():
    adj = {0: [1, 2], 1: [3], 2: [4], 3: [], 4: []}
    order = bfs(adj, 0)
    assert order == [0, 1, 2, 3, 4]

def test_edge_cycle():
    adj = {0: [1], 1: [2], 2: [0]}
    assert bfs(adj, 0) == [0, 1, 2]

def test_edge_missing_start():
    assert bfs({}, 99) == []
""",
        "hints": {
            1: "Use collections.deque for O(1) popleft.",
            2: "Mark vertices visited immediately upon enqueueing to avoid duplicate queue entries.",
            3: "BFS explores nodes in increasing order of shortest distance from start.",
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
        "func": "count_components_dfs",
        "signature": "def count_components_dfs(n: int, edges: list[list[int]]) -> int:",
        "doc": "Count connected components in an undirected graph with n nodes (0 to n-1).",
        "starter": """def count_components_dfs(n: int, edges: list[list[int]]) -> int:
    \"\"\"
    Count connected components in an undirected graph with n nodes (0 to n-1) using DFS.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def count_components_dfs(n: int, edges: list[list[int]]) -> int:
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
""",
        "test": """from tests.loader import load_exercise
import pytest

count_components_dfs = load_exercise("graphs/components_dfs.py", "count_components_dfs")

def test_basic():
    assert count_components_dfs(5, [[0, 1], [1, 2], [3, 4]]) == 2

def test_edge_all_isolated():
    assert count_components_dfs(4, []) == 4

def test_edge_single_component():
    assert count_components_dfs(4, [[0, 1], [1, 2], [2, 3]]) == 1
""",
        "hints": {
            1: "Iterate through 0..n-1; whenever an unvisited vertex is found, trigger a DFS traversal.",
            2: "Increment component count each time a new DFS traversal starts.",
            3: "Graph is undirected: insert both (u, v) and (v, u).",
            4: "Visited set tracks all visited nodes globally across traversals.",
            5: "See reference implementation in reference/graphs/components_dfs.py."
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
        "func": "count_components_bfs",
        "signature": "def count_components_bfs(n: int, edges: list[list[int]]) -> int:",
        "doc": "Count connected components in an undirected graph with n nodes using BFS.",
        "starter": """def count_components_bfs(n: int, edges: list[list[int]]) -> int:
    \"\"\"
    Count connected components in an undirected graph with n nodes using BFS.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """from collections import deque

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
""",
        "test": """from tests.loader import load_exercise
import pytest

count_components_bfs = load_exercise("graphs/components_bfs.py", "count_components_bfs")

def test_basic():
    assert count_components_bfs(5, [[0, 1], [1, 2], [3, 4]]) == 2

def test_edge_zero_edges():
    assert count_components_bfs(3, []) == 3

def test_edge_complete_graph():
    edges = [[0, 1], [1, 2], [0, 2]]
    assert count_components_bfs(3, edges) == 1
""",
        "hints": {
            1: "Use deque for BFS queue within outer loop over 0..n-1.",
            2: "Mark visited upon enqueueing to keep queue minimal.",
            3: "Total time is O(V + E) across all BFS launches.",
            4: "Space is O(V) for visited set and queue.",
            5: "See reference implementation in reference/graphs/components_bfs.py."
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
        "func": "has_cycle_undirected",
        "signature": "def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:",
        "doc": "Determine whether an undirected graph with n nodes (0 to n-1) contains a cycle.",
        "starter": """def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
    \"\"\"
    Determine whether an undirected graph contains a cycle.
    Nodes are numbered 0 through n - 1.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def has_cycle_undirected(n: int, edges: list[list[int]]) -> bool:
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
""",
        "test": """from tests.loader import load_exercise
import pytest

has_cycle_undirected = load_exercise("graphs/cycle_undirected.py", "has_cycle_undirected")

def test_basic_cycle():
    assert has_cycle_undirected(3, [[0, 1], [1, 2], [2, 0]]) is True

def test_basic_tree():
    assert has_cycle_undirected(4, [[0, 1], [1, 2], [2, 3]]) is False

def test_edge_disconnected_cycle():
    assert has_cycle_undirected(5, [[0, 1], [2, 3], [3, 4], [4, 2]]) is True

def test_edge_no_edges():
    assert has_cycle_undirected(3, []) is False
""",
        "hints": {
            1: "In undirected graphs, an edge to an already-visited node is a cycle only if it is NOT the parent.",
            2: "Pass parent pointer in DFS helper: dfs(node, parent).",
            3: "Check all disconnected components by iterating i in range(n).",
            4: "If neighbor in visited and neighbor != parent, cycle detected.",
            5: "See reference implementation in reference/graphs/cycle_undirected.py."
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
        "func": "has_cycle_directed",
        "signature": "def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:",
        "doc": "Determine whether a directed graph contains a cycle using 3-color DFS state.",
        "starter": """def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    \"\"\"
    Determine whether a directed graph contains a cycle.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)

    # 0 = unvisited (white), 1 = visiting/on call stack (gray), 2 = finished (black)
    state = [0] * n

    def dfs(node: int) -> bool:
        state[node] = 1
        for neighbor in adj[node]:
            if state[neighbor] == 1:
                return True  # Back edge found
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
""",
        "test": """from tests.loader import load_exercise
import pytest

has_cycle_directed = load_exercise("graphs/cycle_directed.py", "has_cycle_directed")

def test_basic_cycle():
    assert has_cycle_directed(3, [[0, 1], [1, 2], [2, 0]]) is True

def test_basic_dag():
    assert has_cycle_directed(3, [[0, 1], [0, 2], [1, 2]]) is False

def test_edge_self_loop():
    assert has_cycle_directed(2, [[0, 0]]) is True

def test_edge_disconnected_cycle():
    assert has_cycle_directed(4, [[0, 1], [2, 3], [3, 2]]) is True
""",
        "hints": {
            1: "Use 3 states: 0=unvisited, 1=in current recursion path, 2=fully processed.",
            2: "Encountering a node in state 1 represents a back-edge in the DFS forest, which proves a cycle.",
            3: "Change state back to 2 when exiting DFS for a vertex.",
            4: "Target complexity is O(V + E) time and O(V) space.",
            5: "See reference implementation in reference/graphs/cycle_directed.py."
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
        "func": "topological_sort_dfs",
        "signature": "def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:",
        "doc": "Return valid topological ordering for a DAG using DFS postorder, or empty list if cycle exists.",
        "starter": """def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:
    \"\"\"
    Return a valid topological order of nodes 0 to n-1.
    If the graph contains a cycle, return an empty list.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        adj[u].append(v)

    state = [0] * n  # 0: unvisited, 1: visiting, 2: visited
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
""",
        "test": """from tests.loader import load_exercise
import pytest

topological_sort_dfs = load_exercise("graphs/topo_dfs.py", "topological_sort_dfs")

def verify_topo(n, edges, order):
    if not order:
        return False
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        if pos[u] > pos[v]:
            return False
    return len(order) == n

def test_basic_dag():
    edges = [[0, 1], [0, 2], [1, 3], [2, 3]]
    res = topological_sort_dfs(4, edges)
    assert verify_topo(4, edges, res)

def test_cycle_returns_empty():
    edges = [[0, 1], [1, 2], [2, 0]]
    assert topological_sort_dfs(3, edges) == []

def test_edge_isolated_nodes():
    res = topological_sort_dfs(3, [])
    assert len(res) == 3
    assert set(res) == {0, 1, 2}
""",
        "hints": {
            1: "In DFS topological sort, add node to result upon completion of all its descendants (postorder).",
            2: "Reverse the postorder list at the end to get topological ordering.",
            3: "Detect cycles simultaneously using 3-color state (0/1/2).",
            4: "If a cycle is detected, return [].",
            5: "See reference implementation in reference/graphs/topo_dfs.py."
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
        "func": "topological_sort_kahn",
        "signature": "def topological_sort_kahn(n: int, edges: list[list[int]]) -> list[int]:",
        "doc": "Return topological sort using BFS with in-degree array (Kahn's algorithm).",
        "starter": """from collections import deque

def topological_sort_kahn(n: int, edges: list[list[int]]) -> list[int]:
    \"\"\"
    Return a valid topological order using Kahn's algorithm (in-degree BFS).
    Return empty list if a cycle is present.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """from collections import deque

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
""",
        "test": """from tests.loader import load_exercise
import pytest

topological_sort_kahn = load_exercise("graphs/topo_kahn.py", "topological_sort_kahn")

def verify_topo(n, edges, order):
    if not order or len(order) != n:
        return False
    pos = {node: i for i, node in enumerate(order)}
    for u, v in edges:
        if pos[u] > pos[v]:
            return False
    return True

def test_basic_kahn():
    edges = [[1, 0], [2, 0], [3, 1], [3, 2]]
    order = topological_sort_kahn(4, edges)
    assert verify_topo(4, edges, order)

def test_cycle_detection():
    edges = [[0, 1], [1, 2], [2, 0]]
    assert topological_sort_kahn(3, edges) == []
""",
        "hints": {
            1: "Compute in-degrees of all vertices. Enqueue all vertices with in_degree == 0.",
            2: "When removing node from queue, decrement in-degree of its neighbors.",
            3: "If in-degree of neighbor reaches 0, enqueue it.",
            4: "If order length < n after queue is empty, there is a cycle.",
            5: "See reference implementation in reference/graphs/topo_kahn.py."
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
        "func": "UnionFind",
        "signature": "class UnionFind:",
        "doc": "Disjoint set union data structure supporting find with path compression and union.",
        "starter": """class UnionFind:
    \"\"\"
    Disjoint Set Union with path compression.
    \"\"\"
    def __init__(self, size: int):
        raise NotImplementedError

    def find(self, x: int) -> int:
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def connected(self, x: int, y: int) -> bool:
        raise NotImplementedError
""",
        "reference": """class UnionFind:
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
""",
        "test": """from tests.loader import load_exercise
import pytest

UnionFind = load_exercise("graphs/union_find.py", "UnionFind")

def test_basic_union_find():
    uf = UnionFind(5)
    assert not uf.connected(0, 1)
    assert uf.union(0, 1) is True
    assert uf.connected(0, 1) is True
    assert uf.union(0, 1) is False
    uf.union(1, 2)
    assert uf.connected(0, 2) is True
    assert not uf.connected(0, 3)

def test_chain_compression():
    uf = UnionFind(10)
    for i in range(9):
        uf.union(i, i + 1)
    for i in range(10):
        assert uf.connected(0, i)
""",
        "hints": {
            1: "self.parent[x] = self.find(self.parent[x]) flattens the tree during find.",
            2: "union returns False if x and y already share the same representative root.",
            3: "connected(x, y) simply tests find(x) == find(y).",
            4: "Path compression alone achieves nearly O(1) amortized operations.",
            5: "See reference implementation in reference/graphs/union_find.py."
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
        "func": "UnionFindSize",
        "signature": "class UnionFindSize:",
        "doc": "Union-Find combining both path compression and union by rank/size.",
        "starter": """class UnionFindSize:
    \"\"\"
    Union-Find with path compression and union by size.
    \"\"\"
    def __init__(self, size: int):
        raise NotImplementedError

    def find(self, x: int) -> int:
        raise NotImplementedError

    def union(self, x: int, y: int) -> bool:
        raise NotImplementedError

    def get_component_size(self, x: int) -> int:
        raise NotImplementedError
""",
        "reference": """class UnionFindSize:
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
""",
        "test": """from tests.loader import load_exercise
import pytest

UnionFindSize = load_exercise("graphs/union_find_size.py", "UnionFindSize")

def test_union_by_size():
    uf = UnionFindSize(5)
    assert uf.get_component_size(0) == 1
    uf.union(0, 1)
    assert uf.get_component_size(0) == 2
    assert uf.get_component_size(1) == 2
    uf.union(2, 3)
    uf.union(0, 2)
    assert uf.get_component_size(0) == 4
    assert uf.num_components == 2
""",
        "hints": {
            1: "Attach the smaller tree under the larger tree's root.",
            2: "Update the size of the new root by adding the smaller tree's size.",
            3: "Decrement num_components when union successfully connects two disjoint sets.",
            4: "This combination guarantees O(alpha(N)) inverse Ackermann time complexity.",
            5: "See reference implementation in reference/graphs/union_find_size.py."
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
        "func": "shortest_distance_from_sources",
        "signature": "def shortest_distance_from_sources(grid: list[list[int]]) -> list[list[int]]:",
        "doc": "Find shortest distance from any 1 to every cell in a binary grid using multi-source BFS.",
        "starter": """from collections import deque

def shortest_distance_from_sources(grid: list[list[int]]) -> list[list[int]]:
    \"\"\"
    Given an m x n binary grid where 1 is a source and 0 is an empty cell,
    return a matrix where dist[r][c] is the shortest Manhattan distance to any 1.
    Target Time: O(R * C)
    Target Space: O(R * C)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """from collections import deque

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
""",
        "test": """from tests.loader import load_exercise
import pytest

shortest_distance_from_sources = load_exercise("graphs/multisource_bfs.py", "shortest_distance_from_sources")

def test_basic_multisource():
    grid = [
        [0, 0, 0],
        [0, 1, 0],
        [0, 0, 0]
    ]
    res = shortest_distance_from_sources(grid)
    assert res[1][1] == 0
    assert res[0][1] == 1
    assert res[0][0] == 2

def test_multiple_sources():
    grid = [
        [1, 0],
        [0, 1]
    ]
    res = shortest_distance_from_sources(grid)
    assert res == [[0, 1], [1, 0]]
""",
        "hints": {
            1: "Enqueue all sources (cells with 1) at time 0 initially into the queue.",
            2: "Use dist matrix initialized to -1 to simultaneously track visited cells and distances.",
            3: "Cells are expanded in concentric level rings from all sources simultaneously.",
            4: "Manhattan neighbor directions are (0, 1), (1, 0), (0, -1), (-1, 0).",
            5: "See reference implementation in reference/graphs/multisource_bfs.py."
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
        "func": "num_islands_dfs",
        "signature": "def num_islands_dfs(grid: list[list[str]]) -> int:",
        "doc": "Count connected components of '1's in a 2D grid using DFS.",
        "starter": """def num_islands_dfs(grid: list[list[str]]) -> int:
    \"\"\"
    Count number of islands ('1' surrounded by '0's) using DFS.
    Target Time: O(R * C)
    Target Space: O(R * C)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def num_islands_dfs(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0
    rows, cols = len(grid), len(grid[0])
    visited = set()
    islands = 0

    def dfs(r: int, c: int):
        visited.add((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == '1' and (nr, nc) not in visited:
                dfs(nr, nc)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1' and (r, c) not in visited:
                islands += 1
                dfs(r, c)

    return islands
""",
        "test": """from tests.loader import load_exercise
import pytest

num_islands_dfs = load_exercise("graphs/grid_dfs.py", "num_islands_dfs")

def test_basic_islands():
    grid = [
        ["1", "1", "0", "0"],
        ["1", "1", "0", "0"],
        ["0", "0", "1", "0"],
        ["0", "0", "0", "1"]
    ]
    assert num_islands_dfs(grid) == 3

def test_edge_empty():
    assert num_islands_dfs([]) == 0

def test_edge_all_water():
    assert num_islands_dfs([["0", "0"], ["0", "0"]]) == 0
""",
        "hints": {
            1: "Iterate across all cells; whenever unvisited '1' is encountered, increment island count and DFS sink.",
            2: "Bounds check 0 <= nr < rows and 0 <= nc < cols before recursing.",
            3: "Visited set or mutating grid to '0' avoids revisiting cells.",
            4: "Complexity is O(R * C) as each cell is visited at most 4 times.",
            5: "See reference implementation in reference/graphs/grid_dfs.py."
        }
    },
    {
        "id": "graph-grid-bfs",
        "name": "Grid BFS (Shortest Path in Binary Matrix)",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(R * C)",
        "space_complexity": "O(R * C)",
        "file": "grid_bfs.py",
        "func": "shortest_path_binary_matrix",
        "signature": "def shortest_path_binary_matrix(grid: list[list[int]]) -> int:",
        "doc": "Find length of shortest 8-directional clear path from top-left to bottom-right in binary matrix.",
        "starter": """from collections import deque

def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    \"\"\"
    Return length of shortest 8-directional path from (0,0) to (n-1, n-1) with value 0.
    Return -1 if no path exists.
    Target Time: O(R * C)
    Target Space: O(R * C)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """from collections import deque

def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    if not grid or grid[0][0] != 0 or grid[-1][-1] != 0:
        return -1
    n = len(grid)
    if n == 1:
        return 1

    queue = deque([(0, 0, 1)])  # (r, c, length)
    visited = {(0, 0)}

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

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
""",
        "test": """from tests.loader import load_exercise
import pytest

shortest_path_binary_matrix = load_exercise("graphs/grid_bfs.py", "shortest_path_binary_matrix")

def test_basic_path():
    grid = [[0, 1], [1, 0]]
    assert shortest_path_binary_matrix(grid) == 2

def test_blocked_start_end():
    assert shortest_path_binary_matrix([[1, 0], [0, 0]]) == -1
    assert shortest_path_binary_matrix([[0, 0], [0, 1]]) == -1

def test_no_path():
    grid = [[0, 1, 1], [1, 1, 1], [1, 1, 0]]
    assert shortest_path_binary_matrix(grid) == -1
""",
        "hints": {
            1: "Check if start (0, 0) or end (n-1, n-1) are blocked (value 1); if so return -1.",
            2: "Remember this problem allows 8-directional movement including all 4 diagonals.",
            3: "BFS ensures first arrival at (n-1, n-1) has minimal step count.",
            4: "Mark visited upon pushing into queue to avoid TLE.",
            5: "See reference implementation in reference/graphs/grid_bfs.py."
        }
    },
    {
        "id": "graph-dijkstra",
        "name": "Dijkstra's Shortest Path Algorithm",
        "category": "graphs",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O((V + E) log V)",
        "space_complexity": "O(V)",
        "file": "dijkstra.py",
        "func": "dijkstra",
        "signature": "def dijkstra(n: int, edges: list[list[int]], start: int) -> dict[int, int]:",
        "doc": "Find shortest distance from source to all vertices in a weighted non-negative graph.",
        "starter": """import heapq

def dijkstra(n: int, edges: list[list[int]], start: int) -> dict[int, int]:
    \"\"\"
    Dijkstra's algorithm for single-source shortest paths with non-negative edge weights.
    edges format: [[u, v, weight], ...]
    Returns dict mapping node -> shortest distance (-1 if unreachable).
    Target Time: O((V + E) log V)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """import heapq

def dijkstra(n: int, edges: list[list[int]], start: int) -> dict[int, int]:
    adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))

    distances = {i: -1 for i in range(n)}
    pq = [(0, start)]  # (dist, node)

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if distances[u] != -1:
            continue
        distances[u] = curr_dist
        for v, weight in adj[u]:
            if distances[v] == -1:
                heapq.heappush(pq, (curr_dist + weight, v))

    return distances
""",
        "test": """from tests.loader import load_exercise
import pytest

dijkstra = load_exercise("graphs/dijkstra.py", "dijkstra")

def test_basic_dijkstra():
    edges = [[0, 1, 4], [0, 2, 1], [2, 1, 2], [1, 3, 1]]
    res = dijkstra(4, edges, 0)
    assert res[0] == 0
    assert res[2] == 1
    assert res[1] == 3  # 0->2->1 is cost 3, cheaper than 0->1 cost 4
    assert res[3] == 4

def test_unreachable():
    edges = [[0, 1, 5]]
    res = dijkstra(3, edges, 0)
    assert res[2] == -1
""",
        "hints": {
            1: "Use min-heap storing tuples (distance_so_far, node).",
            2: "Skip popped nodes if they already have an assigned shortest distance.",
            3: "Dijkstra is greedy: once a node is popped, its shortest distance is finalized.",
            4: "Weights must be non-negative for Dijkstra's correctness guarantee.",
            5: "See reference implementation in reference/graphs/dijkstra.py."
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
        "func": "is_bipartite",
        "signature": "def is_bipartite(graph: list[list[int]]) -> bool:",
        "doc": "Determine whether an undirected graph is bipartite using 2-coloring.",
        "starter": """def is_bipartite(graph: list[list[int]]) -> bool:
    \"\"\"
    Determine if an undirected graph is bipartite (2-colorable).
    graph[u] contains list of adjacent vertices for vertex u.
    Target Time: O(V + E)
    Target Space: O(V)
    \"\"\"
    raise NotImplementedError
""",
        "reference": """def is_bipartite(graph: list[list[int]]) -> bool:
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
""",
        "test": """from tests.loader import load_exercise
import pytest

is_bipartite = load_exercise("graphs/bipartite.py", "is_bipartite")

def test_bipartite_even_cycle():
    # 4-cycle is bipartite
    graph = [[1, 3], [0, 2], [1, 3], [0, 2]]
    assert is_bipartite(graph) is True

def test_non_bipartite_odd_cycle():
    # 3-cycle is not bipartite
    graph = [[1, 2], [0, 2], [0, 1]]
    assert is_bipartite(graph) is False

def test_disconnected():
    graph = [[], [2], [1]]
    assert is_bipartite(graph) is True
""",
        "hints": {
            1: "A graph is bipartite if and only if it contains no odd-length cycles.",
            2: "Attempt to 2-color nodes with 0 and 1 using BFS or DFS.",
            3: "If an adjacent neighbor already has the same color as the current vertex, return False.",
            4: "Handle disconnected components by looping over all 0..n-1 vertices.",
            5: "See reference implementation in reference/graphs/bipartite.py."
        }
    },
]

print(f"Loaded {len(EXERCISES)} graph exercises")
