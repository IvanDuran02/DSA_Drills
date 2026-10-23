def rob(nums: list[int]) -> int:
    prev1 = 0  # max excluding previous
    prev2 = 0  # max including previous
    for x in nums:
        new_rob = max(prev2, prev1 + x)
        prev1, prev2 = prev2, new_rob
    return prev2
