import math

def min_eating_speed(piles: list[int], h: int) -> int:
    def can_finish(k: int) -> bool:
        hours = 0
        for p in piles:
            hours += math.ceil(p / k)
        return hours <= h

    left, right = 1, max(piles)
    ans = right
    while left <= right:
        mid = (left + right) // 2
        if can_finish(mid):
            ans = mid
            right = mid - 1
        else:
            left = mid + 1
    return ans
