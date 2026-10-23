def subsets(nums: list[int]) -> list[list[int]]:
    res = []
    subset = []
    def backtrack(start: int):
        res.append(list(subset))
        for i in range(start, len(nums)):
            subset.append(nums[i])
            backtrack(i + 1)
            subset.pop()
    backtrack(0)
    return res
