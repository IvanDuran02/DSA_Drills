def has_cycle_directed(n: int, edges: list[list[int]]) -> bool:
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
