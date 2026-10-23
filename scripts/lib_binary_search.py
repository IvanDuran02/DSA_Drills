"""Binary search algorithm definitions (7 exercises)"""

BINARY_SEARCH_EXERCISES = [
    {
        "id": "binary-search-standard",
        "name": "Standard Binary Search",
        "category": "binary_search",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 6,
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "file": "bs_standard.py",
        "starter": '''def binary_search(nums: list[int], target: int) -> int:
    """
    Search for target in sorted array nums. Return index or -1 if not found.
    Target Time: O(log N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
''',
        "test": '''from tests.loader import load_exercise

binary_search = load_exercise("binary_search/bs_standard.py", "binary_search")

def test_bs():
    nums = [-1, 0, 3, 5, 9, 12]
    assert binary_search(nums, 9) == 4
    assert binary_search(nums, 2) == -1
    assert binary_search([], 5) == -1
''',
        "hints": {
            1: "Maintain inclusive search window [left, right].",
            2: "mid = (left + right) // 2.",
            3: "Shrink window appropriately: left = mid + 1 or right = mid - 1.",
            4: "O(log N) time.",
            5: "See reference in reference/binary_search/bs_standard.py."
        }
    },
    {
        "id": "binary-search-lower-bound",
        "name": "Binary Search Lower Bound",
        "category": "binary_search",
        "difficulty": "Easy",
        "level": 2,
        "recommended_minutes": 8,
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "file": "bs_lower_bound.py",
        "starter": '''def lower_bound(nums: list[int], target: int) -> int:
    """
    Find first index i such that nums[i] >= target. Return len(nums) if all < target.
    Target Time: O(log N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def lower_bound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] >= target:
            right = mid
        else:
            left = mid + 1
    return left
''',
        "test": '''from tests.loader import load_exercise

lower_bound = load_exercise("binary_search/bs_lower_bound.py", "lower_bound")

def test_lb():
    nums = [1, 2, 4, 4, 5, 6]
    assert lower_bound(nums, 4) == 2
    assert lower_bound(nums, 3) == 2
    assert lower_bound(nums, 7) == 6
''',
        "hints": {
            1: "Search range is [0, len(nums)].",
            2: "If nums[mid] >= target: right = mid.",
            3: "Else: left = mid + 1.",
            4: "Loop terminates when left == right.",
            5: "See reference in reference/binary_search/bs_lower_bound.py."
        }
    },
    {
        "id": "binary-search-upper-bound",
        "name": "Binary Search Upper Bound",
        "category": "binary_search",
        "difficulty": "Easy",
        "level": 2,
        "recommended_minutes": 8,
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "file": "bs_upper_bound.py",
        "starter": '''def upper_bound(nums: list[int], target: int) -> int:
    """
    Find first index i such that nums[i] > target. Return len(nums) if none > target.
    Target Time: O(log N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def upper_bound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > target:
            right = mid
        else:
            left = mid + 1
    return left
''',
        "test": '''from tests.loader import load_exercise

upper_bound = load_exercise("binary_search/bs_upper_bound.py", "upper_bound")

def test_ub():
    nums = [1, 2, 4, 4, 5, 6]
    assert upper_bound(nums, 4) == 4
    assert upper_bound(nums, 6) == 6
''',
        "hints": {
            1: "Condition is strictly greater: nums[mid] > target.",
            2: "right = mid when nums[mid] > target.",
            3: "Returns insertion index after duplicates.",
            4: "O(log N) time.",
            5: "See reference in reference/binary_search/bs_upper_bound.py."
        }
    },
    {
        "id": "binary-search-first-last",
        "name": "First and Last Position of Element",
        "category": "binary_search",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "file": "first_last_pos.py",
        "starter": '''def search_range(nums: list[int], target: int) -> list[int]:
    """
    Find starting and ending position of target in sorted array nums.
    Return [-1, -1] if target not found.
    Target Time: O(log N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def search_range(nums: list[int], target: int) -> list[int]:
    def find_first():
        l, r = 0, len(nums) - 1
        res = -1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                res = mid
                r = mid - 1
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return res

    def find_last():
        l, r = 0, len(nums) - 1
        res = -1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                res = mid
                l = mid + 1
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return res

    return [find_first(), find_last()]
''',
        "test": '''from tests.loader import load_exercise

search_range = load_exercise("binary_search/first_last_pos.py", "search_range")

def test_range():
    nums = [5, 7, 7, 8, 8, 10]
    assert search_range(nums, 8) == [3, 4]
    assert search_range(nums, 6) == [-1, -1]
    assert search_range([], 0) == [-1, -1]
''',
        "hints": {
            1: "Perform two separate binary searches: one for lower bound, one for upper bound.",
            2: "To find first, continue searching left (r = mid - 1) on match.",
            3: "To find last, continue searching right (l = mid + 1) on match.",
            4: "O(log N) total time.",
            5: "See reference in reference/binary_search/first_last_pos.py."
        }
    },
    {
        "id": "binary-search-rotated",
        "name": "Search in Rotated Sorted Array",
        "category": "binary_search",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "file": "bs_rotated.py",
        "starter": '''def search_rotated(nums: list[int], target: int) -> int:
    """
    Search in rotated sorted array of distinct elements. Return index or -1.
    Target Time: O(log N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def search_rotated(nums: list[int], target: int) -> int:
    l, r = 0, len(nums) - 1
    while l <= r:
        mid = (l + r) // 2
        if nums[mid] == target:
            return mid
        # Check if left half is sorted
        if nums[l] <= nums[mid]:
            if nums[l] <= target < nums[mid]:
                r = mid - 1
            else:
                l = mid + 1
        else: # Right half is sorted
            if nums[mid] < target <= nums[r]:
                l = mid + 1
            else:
                r = mid - 1
    return -1
''',
        "test": '''from tests.loader import load_exercise

search_rotated = load_exercise("binary_search/bs_rotated.py", "search_rotated")

def test_rotated():
    nums = [4, 5, 6, 7, 0, 1, 2]
    assert search_rotated(nums, 0) == 4
    assert search_rotated(nums, 3) == -1
''',
        "hints": {
            1: "At least one half [left, mid] or [mid, right] is always normally sorted.",
            2: "Determine which half is sorted using nums[l] <= nums[mid].",
            3: "Check if target falls within the sorted half's boundaries.",
            4: "O(log N) time.",
            5: "See reference in reference/binary_search/bs_rotated.py."
        }
    },
    {
        "id": "binary-search-on-answer",
        "name": "Binary Search on Answer (Koko Eating Bananas)",
        "category": "binary_search",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(N log(max(P)))",
        "space_complexity": "O(1)",
        "file": "bs_on_answer.py",
        "starter": '''def min_eating_speed(piles: list[int], h: int) -> int:
    """
    Find minimum integer speed k to eat all bananas within h hours.
    Target Time: O(N log(max(piles)))
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''import math

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
''',
        "test": '''from tests.loader import load_exercise

min_eating_speed = load_exercise("binary_search/bs_on_answer.py", "min_eating_speed")

def test_koko():
    assert min_eating_speed([3, 6, 7, 11], 8) == 4
    assert min_eating_speed([30, 11, 23, 4, 20], 5) == 30
''',
        "hints": {
            1: "Search space is speed range: 1 to max(piles).",
            2: "Monotonic predicate: if can finish at speed k, can finish at any speed > k.",
            3: "Find minimal valid speed with lower bound search.",
            4: "Hours to eat pile p at speed k is ceil(p / k) or (p + k - 1) // k.",
            5: "See reference in reference/binary_search/bs_on_answer.py."
        }
    },
    {
        "id": "binary-search-min-rotated",
        "name": "Find Minimum in Rotated Sorted Array",
        "category": "binary_search",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "file": "bs_min_rotated.py",
        "starter": '''def find_min(nums: list[int]) -> int:
    """
    Find minimum element in rotated sorted array of unique elements.
    Target Time: O(log N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def find_min(nums: list[int]) -> int:
    left, right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > nums[right]:
            left = mid + 1
        else:
            right = mid
    return nums[left]
''',
        "test": '''from tests.loader import load_exercise

find_min = load_exercise("binary_search/bs_min_rotated.py", "find_min")

def test_min_rotated():
    assert find_min([3, 4, 5, 1, 2]) == 1
    assert find_min([4, 5, 6, 7, 0, 1, 2]) == 0
    assert find_min([11, 13, 15, 17]) == 11
''',
        "hints": {
            1: "Compare nums[mid] against nums[right].",
            2: "If nums[mid] > nums[right], minimum lies in right half: left = mid + 1.",
            3: "Else, minimum lies at mid or to the left: right = mid.",
            4: "Loop ends when left == right.",
            5: "See reference in reference/binary_search/bs_min_rotated.py."
        }
    }
]
