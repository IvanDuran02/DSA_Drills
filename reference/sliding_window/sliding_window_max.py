from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    if not nums or k <= 0:
        return []
    deq = deque()  # stores indices in monotonically decreasing value order
    res = []
    for i, x in enumerate(nums):
        # Remove elements outside current window
        if deq and deq[0] < i - k + 1:
            deq.popleft()
        # Maintain decreasing order
        while deq and nums[deq[-1]] < x:
            deq.pop()
        deq.append(i)
        if i >= k - 1:
            res.append(nums[deq[0]])
    return res
