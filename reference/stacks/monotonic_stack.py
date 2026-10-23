def previous_smaller_element(nums: list[int]) -> list[int]:
    res = [-1] * len(nums)
    stack = []  # increasing stack of values
    for i, x in enumerate(nums):
        while stack and stack[-1] >= x:
            stack.pop()
        if stack:
            res[i] = stack[-1]
        stack.append(x)
    return res
