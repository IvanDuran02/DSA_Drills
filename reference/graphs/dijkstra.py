import heapq

def dijkstra(n: int, edges: list[list[int]], start: int) -> dict[int, int]:
    adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(n)}
    for u, v, w in edges:
        adj[u].append((v, w))

    distances = {i: -1 for i in range(n)}
    pq = [(0, start)]

    while pq:
        curr_dist, u = heapq.heappop(pq)
        if distances[u] != -1:
            continue
        distances[u] = curr_dist
        for v, weight in adj[u]:
            if distances[v] == -1:
                heapq.heappush(pq, (curr_dist + weight, v))

    return distances
