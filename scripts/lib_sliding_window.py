"""Sliding Window, Two Pointers, and Prefix Sums definitions (10 exercises)"""

SLIDING_WINDOW_EXERCISES = [
    {
        "id": "sliding-window-fixed",
        "name": "Fixed-Size Sliding Window (Max Sum Subarray)",
        "category": "sliding_window",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "fixed_window.py",
        "starter": '''def max_sum_subarray(nums: list[int], k: int) -> int:
    """
    Find maximum sum of any contiguous subarray of size k.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def max_sum_subarray(nums: list[int], k: int) -> int:
    if not nums or k <= 0 or len(nums) < k:
        return 0
    curr_sum = sum(nums[:k])
    max_sum = curr_sum
    for i in range(k, len(nums)):
        curr_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, curr_sum)
    return max_sum
''',
        "test": '''from tests.loader import load_exercise

max_sum_subarray = load_exercise("sliding_window/fixed_window.py", "max_sum_subarray")

def test_fixed():
    assert max_sum_subarray([2, 1, 5, 1, 3, 2], 3) == 9
    assert max_sum_subarray([1, 2], 3) == 0
''',
        "hints": {
            1: "Calculate sum of first k elements.",
            2: "Slide window by adding nums[i] and subtracting nums[i - k].",
            3: "Tracks max in O(N) time with O(1) extra space.",
            4: "Handles empty or k > len(nums) edge case.",
            5: "See reference in reference/sliding_window/fixed_window.py."
        }
    },
    {
        "id": "sliding-window-variable",
        "name": "Minimum Size Subarray Sum",
        "category": "sliding_window",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "variable_window.py",
        "starter": '''def min_sub_array_len(target: int, nums: list[int]) -> int:
    """
    Find minimal length of contiguous subarray with sum >= target. Return 0 if none.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def min_sub_array_len(target: int, nums: list[int]) -> int:
    left = 0
    curr_sum = 0
    min_len = float('inf')
    for right in range(len(nums)):
        curr_sum += nums[right]
        while curr_sum >= target:
            min_len = min(min_len, right - left + 1)
            curr_sum -= nums[left]
            left += 1
    return min_len if min_len != float('inf') else 0
''',
        "test": '''from tests.loader import load_exercise

min_sub_array_len = load_exercise("sliding_window/variable_window.py", "min_sub_array_len")

def test_var_window():
    assert min_sub_array_len(7, [2, 3, 1, 2, 4, 3]) == 2
    assert min_sub_array_len(4, [1, 4, 4]) == 1
    assert min_sub_array_len(11, [1, 1, 1, 1, 1]) == 0
''',
        "hints": {
            1: "Expand right pointer, accumulating curr_sum.",
            2: "While curr_sum >= target, update min_len and contract left pointer.",
            3: "Each element is visited at most twice.",
            4: "O(N) time, O(1) space.",
            5: "See reference in reference/sliding_window/variable_window.py."
        }
    },
    {
        "id": "sliding-window-longest-substring",
        "name": "Longest Substring Without Repeating Characters",
        "category": "sliding_window",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(min(N, Sigma))",
        "file": "longest_unique_substr.py",
        "starter": '''def length_of_longest_substring(s: str) -> int:
    """
    Find length of longest substring without repeating characters.
    Target Time: O(N)
    Target Space: O(min(N, Sigma))
    """
    raise NotImplementedError
''',
        "reference": '''def length_of_longest_substring(s: str) -> int:
    char_index = {}
    max_len = 0
    left = 0
    for right, ch in enumerate(s):
        if ch in char_index and char_index[ch] >= left:
            left = char_index[ch] + 1
        char_index[ch] = right
        max_len = max(max_len, right - left + 1)
    return max_len
''',
        "test": '''from tests.loader import load_exercise

length_of_longest_substring = load_exercise("sliding_window/longest_unique_substr.py", "length_of_longest_substring")

def test_longest_substr():
    assert length_of_longest_substring("abcabcbb") == 3
    assert length_of_longest_substring("bbbbb") == 1
    assert length_of_longest_substring("pwwkew") == 3
''',
        "hints": {
            1: "Map each character to its most recent index.",
            2: "If char is seen and char_index[ch] >= left, jump left to char_index[ch] + 1.",
            3: "Window length is right - left + 1.",
            4: "O(N) time with one pass.",
            5: "See reference in reference/sliding_window/longest_unique_substr.py."
        }
    },
    {
        "id": "sliding-window-min-window",
        "name": "Minimum Window Substring",
        "category": "sliding_window",
        "difficulty": "Hard",
        "level": 3,
        "recommended_minutes": 18,
        "time_complexity": "O(M + N)",
        "space_complexity": "O(Sigma)",
        "file": "min_window_substr.py",
        "starter": '''def min_window(s: str, t: str) -> str:
    """
    Find minimum window in s which contains all characters in t.
    Return empty string if no such window exists.
    Target Time: O(M + N)
    Target Space: O(Sigma)
    """
    raise NotImplementedError
''',
        "reference": '''from collections import Counter

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
''',
        "test": '''from tests.loader import load_exercise

min_window = load_exercise("sliding_window/min_window_substr.py", "min_window")

def test_min_window():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "a") == "a"
    assert min_window("a", "aa") == ""
''',
        "hints": {
            1: "Counter(t) defines character needs.",
            2: "Track 'formed' match count to compare against len(need).",
            3: "Shrink window from left while valid.",
            4: "O(M + N) time.",
            5: "See reference in reference/sliding_window/min_window_substr.py."
        }
    },
    {
        "id": "two-pointers-two-sum-sorted",
        "name": "Two Sum II (Input Array Is Sorted)",
        "category": "sliding_window",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "two_sum_sorted.py",
        "starter": '''def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    """
    Find two numbers in 1-indexed sorted array that add up to target.
    Return [index1, index2].
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def two_sum_sorted(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1
    while left < right:
        curr = numbers[left] + numbers[right]
        if curr == target:
            return [left + 1, right + 1]
        elif curr < target:
            left += 1
        else:
            right -= 1
    return []
''',
        "test": '''from tests.loader import load_exercise

two_sum_sorted = load_exercise("sliding_window/two_sum_sorted.py", "two_sum_sorted")

def test_two_sum():
    assert two_sum_sorted([2, 7, 11, 15], 9) == [1, 2]
    assert two_sum_sorted([2, 3, 4], 6) == [1, 3]
''',
        "hints": {
            1: "Inward-facing two pointers: left=0, right=len-1.",
            2: "If sum < target: left += 1.",
            3: "If sum > target: right -= 1.",
            4: "O(N) time, O(1) space.",
            5: "See reference in reference/sliding_window/two_sum_sorted.py."
        }
    },
    {
        "id": "two-pointers-three-sum",
        "name": "3Sum (Zero Sum Triplets)",
        "category": "sliding_window",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(N^2)",
        "space_complexity": "O(1) extra",
        "file": "three_sum.py",
        "starter": '''def three_sum(nums: list[int]) -> list[list[int]]:
    """
    Find all unique triplets in nums that sum to 0.
    Target Time: O(N^2)
    Target Space: O(1) auxiliary
    """
    raise NotImplementedError
''',
        "reference": '''def three_sum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total == 0:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1
    return res
''',
        "test": '''from tests.loader import load_exercise

three_sum = load_exercise("sliding_window/three_sum.py", "three_sum")

def test_three_sum():
    res = three_sum([-1, 0, 1, 2, -1, -4])
    assert sorted(res) == [[-1, -1, 2], [-1, 0, 1]]
    assert three_sum([0, 1, 1]) == []
''',
        "hints": {
            1: "Sort nums first.",
            2: "Fix nums[i] and use two pointers for remaining two elements.",
            3: "Skip duplicates for i, left, and right pointers.",
            4: "O(N^2) time.",
            5: "See reference in reference/sliding_window/three_sum.py."
        }
    },
    {
        "id": "two-pointers-fast-slow",
        "name": "Linked List Cycle Detection (Floyd's Algorithm)",
        "category": "sliding_window",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "fast_slow_pointers.py",
        "starter": '''from typing import Optional
from drills.structures import ListNode

def has_cycle(head: Optional[ListNode]) -> bool:
    """
    Determine if linked list has a cycle using fast and slow pointers.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''from typing import Optional
from reference.structures import ListNode

def has_cycle(head: Optional[ListNode]) -> bool:
    if not head or not head.next:
        return False
    slow = head
    fast = head.next
    while fast and fast.next:
        if slow == fast:
            return True
        slow = slow.next
        fast = fast.next.next
    return False
''',
        "test": '''from tests.loader import load_exercise
from drills.structures import ListNode

has_cycle = load_exercise("sliding_window/fast_slow_pointers.py", "has_cycle")

def test_cycle():
    n1 = ListNode(3)
    n2 = ListNode(2)
    n3 = ListNode(0)
    n4 = ListNode(-4)
    n1.next = n2
    n2.next = n3
    n3.next = n4
    n4.next = n2  # cycle back to n2
    assert has_cycle(n1) is True
    assert has_cycle(ListNode(1)) is False
''',
        "hints": {
            1: "Slow moves 1 step, fast moves 2 steps.",
            2: "If there is a cycle, fast will eventually overtake and meet slow.",
            3: "If fast reaches None, there is no cycle.",
            4: "O(1) extra space.",
            5: "See reference in reference/sliding_window/fast_slow_pointers.py."
        }
    },
    {
        "id": "prefix-sum-basic",
        "name": "Range Sum Query (Prefix Sums)",
        "category": "sliding_window",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N) build, O(1) query",
        "space_complexity": "O(N)",
        "file": "prefix_sum_basic.py",
        "starter": '''class NumArray:
    """
    Range Sum Query using prefix sums.
    """
    def __init__(self, nums: list[int]):
        raise NotImplementedError

    def sum_range(self, left: int, right: int) -> int:
        raise NotImplementedError
''',
        "reference": '''class NumArray:
    def __init__(self, nums: list[int]):
        self.prefix = [0] * (len(nums) + 1)
        for i, x in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + x

    def sum_range(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
''',
        "test": '''from tests.loader import load_exercise

NumArray = load_exercise("sliding_window/prefix_sum_basic.py", "NumArray")

def test_num_array():
    na = NumArray([-2, 0, 3, -5, 2, -1])
    assert na.sum_range(0, 2) == 1
    assert na.sum_range(2, 5) == -1
    assert na.sum_range(0, 5) == -3
''',
        "hints": {
            1: "Build prefix sum array with size N + 1 where prefix[0] = 0.",
            2: "sum_range(left, right) is prefix[right + 1] - prefix[left].",
            3: "O(1) query time.",
            4: "O(N) space.",
            5: "See reference in reference/sliding_window/prefix_sum_basic.py."
        }
    },
    {
        "id": "prefix-sum-hashmap",
        "name": "Subarray Sum Equals K (Prefix Sum + Hashmap)",
        "category": "sliding_window",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "prefix_sum_hashmap.py",
        "starter": '''def subarray_sum(nums: list[int], k: int) -> int:
    """
    Find total number of subarrays whose sum equals k.
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def subarray_sum(nums: list[int], k: int) -> int:
    prefix_counts = {0: 1}
    curr_sum = 0
    count = 0
    for x in nums:
        curr_sum += x
        diff = curr_sum - k
        if diff in prefix_counts:
            count += prefix_counts[diff]
        prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1
    return count
''',
        "test": '''from tests.loader import load_exercise

subarray_sum = load_exercise("sliding_window/prefix_sum_hashmap.py", "subarray_sum")

def test_sub_sum():
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, 2, 3], 3) == 2
    assert subarray_sum([1, -1, 0], 0) == 3
''',
        "hints": {
            1: "prefix[j] - prefix[i] == k <=> prefix[i] == prefix[j] - k.",
            2: "Store frequency of observed prefix sums in hashmap.",
            3: "Initialize hashmap with {0: 1} to handle prefix sum exactly equal to k.",
            4: "O(N) time with one pass.",
            5: "See reference in reference/sliding_window/prefix_sum_hashmap.py."
        }
    },
    {
        "id": "sliding-window-maximum",
        "name": "Sliding Window Maximum (Monotonic Deque)",
        "category": "sliding_window",
        "difficulty": "Hard",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(N)",
        "space_complexity": "O(K)",
        "file": "sliding_window_max.py",
        "starter": '''from collections import deque

def max_sliding_window(nums: list[int], k: int) -> list[int]:
    """
    Find sliding window maximum of array nums with window size k.
    Target Time: O(N)
    Target Space: O(K)
    """
    raise NotImplementedError
''',
        "reference": '''from collections import deque

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
''',
        "test": '''from tests.loader import load_exercise

max_sliding_window = load_exercise("sliding_window/sliding_window_max.py", "max_sliding_window")

def test_window_max():
    nums = [1, 3, -1, -3, 5, 3, 6, 7]
    assert max_sliding_window(nums, 3) == [3, 3, 5, 5, 6, 7]
''',
        "hints": {
            1: "Store indices in deque with values in strictly decreasing order.",
            2: "Pop indices from front when deq[0] < i - k + 1.",
            3: "Pop indices from back when nums[deq[-1]] < current element.",
            4: "Current window max is always nums[deq[0]].",
            5: "See reference in reference/sliding_window/sliding_window_max.py."
        }
    }
]
