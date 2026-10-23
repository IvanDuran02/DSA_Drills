def is_bipartite(graph: list[list[int]]) -> bool:
    n = len(graph)
    color = {}

    for i in range(n):
        if i not in color:
            color[i] = 0
            stack = [i]
            while stack:
                u = stack.pop()
                for v in graph[u]:
                    if v not in color:
                        color[v] = 1 - color[u]
                        stack.append(v)
                    elif color[v] == color[u]:
                        return False
    return True
