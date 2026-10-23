from collections import Counter

def min_window(s: str, t: str) -> str:
    if not s or not t:
        return ""
    need = Counter(t)
    have = {}
    required = len(need)
    formed = 0

    best_len = float('inf')
    best_range = (0, 0)
    left = 0

    for right, ch in enumerate(s):
        have[ch] = have.get(ch, 0) + 1
        if ch in need and have[ch] == need[ch]:
            formed += 1

        while formed == required and left <= right:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best_range = (left, right + 1)

            left_ch = s[left]
            have[left_ch] -= 1
            if left_ch in need and have[left_ch] < need[left_ch]:
                formed -= 1
            left += 1

    return s[best_range[0]:best_range[1]] if best_len != float('inf') else ""
