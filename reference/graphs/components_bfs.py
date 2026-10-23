from collections import deque

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
