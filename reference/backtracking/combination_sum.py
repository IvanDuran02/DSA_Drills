def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    res = []
    candidates.sort()
    comb = []
    def backtrack(start: int, remain: int):
        if remain == 0:
            res.append(list(comb))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            comb.append(candidates[i])
            backtrack(i, remain - candidates[i])
            comb.pop()
    backtrack(0, target)
    return res
