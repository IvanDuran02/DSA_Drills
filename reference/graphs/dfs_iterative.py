def dfs_iterative(adj: dict[int, list[int]], start: int) -> list[int]:
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
