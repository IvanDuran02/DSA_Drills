def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    subset = []
    def backtrack(start: int):
        res.append(list(subset))
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            subset.append(nums[i])
            backtrack(i + 1)
            subset.pop()
    backtrack(0)
    return res
