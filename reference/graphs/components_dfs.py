def count_components_dfs(n: int, edges: list[list[int]]) -> int:
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
