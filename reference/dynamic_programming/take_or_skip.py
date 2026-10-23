def can_partition_sum(nums: list[int], target: int) -> bool:
    memo = {}
    def dfs(i: int, remain: int) -> bool:
        if remain == 0:
            return True
        if i == len(nums) or remain < 0:
            return False
        state = (i, remain)
        if state in memo:
            return memo[state]
        # Take or skip
        ans = dfs(i + 1, remain - nums[i]) or dfs(i + 1, remain)
        memo[state] = ans
        return ans
    return dfs(0, target)
