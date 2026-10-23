def dfs_recursive(adj: dict[int, list[int]], start: int) -> list[int]:
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
