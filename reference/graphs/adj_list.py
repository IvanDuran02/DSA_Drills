def build_adj_list(n: int, edges: list[list[int]], directed: bool = False) -> dict[int, list[int]]:
    adj: dict[int, list[int]] = {i: [] for i in range(n)}
    for u, v in edges:
        if 0 <= u < n and 0 <= v < n:
            adj[u].append(v)
            if not directed:
                adj[v].append(u)
    return adj
