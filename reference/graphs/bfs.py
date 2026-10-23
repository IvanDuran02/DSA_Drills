from collections import deque

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
