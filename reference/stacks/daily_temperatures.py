def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    res = [0] * n
    stack = []  # stores indices with decreasing temperatures
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_idx = stack.pop()
            res[prev_idx] = i - prev_idx
        stack.append(i)
    return res
