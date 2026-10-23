def max_sum_subarray(nums: list[int], k: int) -> int:
    if not nums or k <= 0 or len(nums) < k:
        return 0
    curr_sum = sum(nums[:k])
    max_sum = curr_sum
    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, curr_sum)
    return max_sum
