def next_greater_elements(nums: list[int]) -> list[int]:
    n = len(nums)
    res = [-1] * n
    stack = []  # indices
    for i in range(2 * n):
        curr = nums[i % n]
        while stack and nums[stack[-1]] < curr:
            idx = stack.pop()
            res[idx] = curr
        if i < n:
            stack.append(i)
    return res
