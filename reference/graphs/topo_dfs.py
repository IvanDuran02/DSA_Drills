def topological_sort_dfs(n: int, edges: list[list[int]]) -> list[int]:
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
