def combine(n: int, k: int) -> list[list[int]]:
    res = []
    comb = []
    def backtrack(start: int):
        if len(comb) == k:
            res.append(list(comb))
            return
        # Pruning: need (k - len(comb)) more elements
        needed = k - len(comb)
        for i in range(start, n - needed + 2):
            comb.append(i)
            backtrack(i + 1)
            comb.pop()
    backtrack(1)
    return res
