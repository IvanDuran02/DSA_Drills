def combine(n: int, k: int) -> list[list[int]]:
    """
    Return all combinations of k numbers chosen from range 1 to n.
    Target Time: O(k * C(n, k))
    Target Space: O(k)
    """

    # Basically give all combinations through dfs backtrack

    res = []
    path = []

    def dfs(start):
        if len(path) == 2:
            res.append(path.copy())
        if len(path) > 2:
            return

        for i in range(start, n):
            path.append(i)

            dfs(i + 1)

            path.pop()

    dfs(0)
    return res
