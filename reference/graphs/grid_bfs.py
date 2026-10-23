from collections import deque

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
