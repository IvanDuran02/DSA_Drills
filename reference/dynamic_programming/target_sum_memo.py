def find_target_sum_ways(nums: list[int], target: int) -> int:
    memo = {}
    def dfs(i: int, current_sum: int) -> int:
        if i == len(nums):
            return 1 if current_sum == target else 0
        state = (i, current_sum)
        if state in memo:
            return memo[state]
        ways = dfs(i + 1, current_sum + nums[i]) + dfs(i + 1, current_sum - nums[i])
        memo[state] = ways
        return ways
    return dfs(0, 0)
