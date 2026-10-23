"""Dynamic Programming algorithm definitions (14 exercises)"""

DP_EXERCISES = [
    {
        "id": "dp-fibonacci-memo",
        "name": "Fibonacci (Top-Down Memoization)",
        "category": "dynamic_programming",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 6,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "fib_memo.py",
        "starter": '''def fib_memo(n: int) -> int:
    """
    Compute nth Fibonacci number using top-down recursion with memoization.
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def fib_memo(n: int) -> int:
    memo = {0: 0, 1: 1}
    def helper(k: int) -> int:
        if k not in memo:
            memo[k] = helper(k - 1) + helper(k - 2)
        return memo[k]
    return helper(n)
''',
        "test": '''from tests.loader import load_exercise

fib_memo = load_exercise("dynamic_programming/fib_memo.py", "fib_memo")

def test_fib_memo():
    assert fib_memo(0) == 0
    assert fib_memo(1) == 1
    assert fib_memo(10) == 55
''',
        "hints": {
            1: "Cache results in dict or array.",
            2: "Base cases: 0 -> 0, 1 -> 1.",
            3: "helper(k - 1) + helper(k - 2).",
            4: "Reduces 2^N tree to linear N evaluations.",
            5: "See reference in reference/dynamic_programming/fib_memo.py."
        }
    },
    {
        "id": "dp-fibonacci-tab",
        "name": "Fibonacci (Bottom-Up Tabulation)",
        "category": "dynamic_programming",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 6,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "fib_tab.py",
        "starter": '''def fib_tab(n: int) -> int:
    """
    Compute nth Fibonacci number using bottom-up iteration with O(1) space.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def fib_tab(n: int) -> int:
    if n <= 1:
        return n
    prev, curr = 0, 1
    for _ in range(2, n + 1):
        prev, curr = curr, prev + curr
    return curr
''',
        "test": '''from tests.loader import load_exercise

fib_tab = load_exercise("dynamic_programming/fib_tab.py", "fib_tab")

def test_fib_tab():
    assert fib_tab(0) == 0
    assert fib_tab(1) == 1
    assert fib_tab(10) == 55
''',
        "hints": {
            1: "Iterate from 2 up to n.",
            2: "Keep two variables: prev and curr.",
            3: "Space complexity is O(1).",
            4: "Time complexity is O(N).",
            5: "See reference in reference/dynamic_programming/fib_tab.py."
        }
    },
    {
        "id": "dp-climbing-stairs",
        "name": "Climbing Stairs",
        "category": "dynamic_programming",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 6,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "climbing_stairs.py",
        "starter": '''def climb_stairs(n: int) -> int:
    """
    Find distinct ways to climb n stairs taking 1 or 2 steps.
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b
''',
        "test": '''from tests.loader import load_exercise

climb_stairs = load_exercise("dynamic_programming/climbing_stairs.py", "climb_stairs")

def test_stairs():
    assert climb_stairs(2) == 2
    assert climb_stairs(3) == 3
    assert climb_stairs(5) == 8
''',
        "hints": {
            1: "ways(n) = ways(n - 1) + ways(n - 2).",
            2: "Base cases: 1 stair -> 1 way, 2 stairs -> 2 ways.",
            3: "Fibonacci pattern.",
            4: "O(1) space.",
            5: "See reference in reference/dynamic_programming/climbing_stairs.py."
        }
    },
    {
        "id": "dp-house-robber",
        "name": "House Robber",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "house_robber.py",
        "starter": '''def rob(nums: list[int]) -> int:
    """
    Determine max money that can be robbed without alerting police (no two adjacent houses).
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def rob(nums: list[int]) -> int:
    prev1 = 0  # max excluding previous
    prev2 = 0  # max including previous
    for x in nums:
        new_rob = max(prev2, prev1 + x)
        prev1, prev2 = prev2, new_rob
    return prev2
''',
        "test": '''from tests.loader import load_exercise

rob = load_exercise("dynamic_programming/house_robber.py", "rob")

def test_rob():
    assert rob([1, 2, 3, 1]) == 4
    assert rob([2, 7, 9, 3, 1]) == 12
''',
        "hints": {
            1: "At house i, choose max(rob(i-1), rob(i-2) + nums[i]).",
            2: "Keep two variables to track previous two max amounts.",
            3: "O(N) time with O(1) space.",
            4: "Handles empty list safely.",
            5: "See reference in reference/dynamic_programming/house_robber.py."
        }
    },
    {
        "id": "dp-coin-change",
        "name": "Coin Change (Fewest Coins)",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(amount * len(coins))",
        "space_complexity": "O(amount)",
        "file": "coin_change.py",
        "starter": '''def coin_change(coins: list[int], amount: int) -> int:
    """
    Find fewest coins needed to make up amount. Return -1 if impossible.
    Target Time: O(amount * len(coins))
    Target Space: O(amount)
    """
    raise NotImplementedError
''',
        "reference": '''def coin_change(coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != float('inf') else -1
''',
        "test": '''from tests.loader import load_exercise

coin_change = load_exercise("dynamic_programming/coin_change.py", "coin_change")

def test_coin_change():
    assert coin_change([1, 2, 5], 11) == 3
    assert coin_change([2], 3) == -1
    assert coin_change([1], 0) == 0
''',
        "hints": {
            1: "dp[x] represents min coins to make amount x.",
            2: "dp[0] = 0, others float('inf').",
            3: "dp[x] = min(dp[x], dp[x - coin] + 1).",
            4: "Return -1 if dp[amount] remains infinity.",
            5: "See reference in reference/dynamic_programming/coin_change.py."
        }
    },
    {
        "id": "dp-knapsack-01",
        "name": "0/1 Knapsack Problem",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(N * W)",
        "space_complexity": "O(W)",
        "file": "knapsack_01.py",
        "starter": '''def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    """
    Find max value achievable with given capacity where each item can be taken at most once.
    Target Time: O(N * W)
    Target Space: O(W)
    """
    raise NotImplementedError
''',
        "reference": '''def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    dp = [0] * (capacity + 1)
    for w, v in zip(weights, values):
        for cap in range(capacity, w - 1, -1):
            dp[cap] = max(dp[cap], dp[cap - w] + v)
    return dp[capacity]
''',
        "test": '''from tests.loader import load_exercise

knapsack_01 = load_exercise("dynamic_programming/knapsack_01.py", "knapsack_01")

def test_knapsack():
    weights = [1, 3, 4, 5]
    values = [1, 4, 5, 7]
    assert knapsack_01(weights, values, 7) == 9
''',
        "hints": {
            1: "Iterate capacity backwards to avoid using same item multiple times in 1D array.",
            2: "dp[cap] = max(dp[cap], dp[cap - w] + v).",
            3: "Range goes from capacity down to w.",
            4: "O(N * W) time, O(W) space.",
            5: "See reference in reference/dynamic_programming/knapsack_01.py."
        }
    },
    {
        "id": "dp-lcs",
        "name": "Longest Common Subsequence",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(M * N)",
        "space_complexity": "O(M * N)",
        "file": "lcs.py",
        "starter": '''def longest_common_subsequence(text1: str, text2: str) -> int:
    """
    Find length of longest common subsequence of text1 and text2.
    Target Time: O(M * N)
    Target Space: O(M * N)
    """
    raise NotImplementedError
''',
        "reference": '''def longest_common_subsequence(text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
''',
        "test": '''from tests.loader import load_exercise

longest_common_subsequence = load_exercise("dynamic_programming/lcs.py", "longest_common_subsequence")

def test_lcs():
    assert longest_common_subsequence("abcde", "ace") == 3
    assert longest_common_subsequence("abc", "def") == 0
''',
        "hints": {
            1: "2D table of size (M+1) x (N+1).",
            2: "If text1[i-1] == text2[j-1]: dp[i][j] = dp[i-1][j-1] + 1.",
            3: "Else dp[i][j] = max(dp[i-1][j], dp[i][j-1]).",
            4: "O(M * N) time.",
            5: "See reference in reference/dynamic_programming/lcs.py."
        }
    },
    {
        "id": "dp-lis",
        "name": "Longest Increasing Subsequence",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(N log N) or O(N^2)",
        "space_complexity": "O(N)",
        "file": "lis.py",
        "starter": '''import bisect

def length_of_lis(nums: list[int]) -> int:
    """
    Find length of longest strictly increasing subsequence.
    Target Time: O(N log N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''import bisect

def length_of_lis(nums: list[int]) -> int:
    tails = []
    for x in nums:
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
    return len(tails)
''',
        "test": '''from tests.loader import load_exercise

length_of_lis = load_exercise("dynamic_programming/lis.py", "length_of_lis")

def test_lis():
    assert length_of_lis([10, 9, 2, 5, 3, 7, 101, 18]) == 4
    assert length_of_lis([0, 1, 0, 3, 2, 3]) == 4
    assert length_of_lis([7, 7, 7]) == 1
''',
        "hints": {
            1: "Patience sorting / tails array.",
            2: "bisect_left finds smallest tail >= x.",
            3: "Append if larger than all tails; otherwise replace tail[idx].",
            4: "len(tails) is optimal LIS length in O(N log N).",
            5: "See reference in reference/dynamic_programming/lis.py."
        }
    },
    {
        "id": "dp-unique-paths",
        "name": "Grid Unique Paths",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(M * N)",
        "space_complexity": "O(N)",
        "file": "unique_paths.py",
        "starter": '''def unique_paths(m: int, n: int) -> int:
    """
    Find number of possible unique paths from top-left to bottom-right of m x n grid.
    Only allowed moves: Right and Down.
    Target Time: O(M * N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def unique_paths(m: int, n: int) -> int:
    row = [1] * n
    for _ in range(m - 1):
        for j in range(1, n):
            row[j] += row[j - 1]
    return row[-1]
''',
        "test": '''from tests.loader import load_exercise

unique_paths = load_exercise("dynamic_programming/unique_paths.py", "unique_paths")

def test_paths():
    assert unique_paths(3, 7) == 28
    assert unique_paths(3, 2) == 3
''',
        "hints": {
            1: "dp[i][j] = dp[i-1][j] + dp[i][j-1].",
            2: "Can be compressed into 1D array of size n.",
            3: "Base case: top row and left column are all 1.",
            4: "O(M * N) time, O(N) space.",
            5: "See reference in reference/dynamic_programming/unique_paths.py."
        }
    },
    {
        "id": "dp-edit-distance",
        "name": "Edit Distance (Levenshtein)",
        "category": "dynamic_programming",
        "difficulty": "Hard",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(M * N)",
        "space_complexity": "O(M * N)",
        "file": "edit_distance.py",
        "starter": '''def min_distance(word1: str, word2: str) -> int:
    """
    Find minimum number of operations (insert, delete, replace) to convert word1 to word2.
    Target Time: O(M * N)
    Target Space: O(M * N)
    """
    raise NotImplementedError
''',
        "reference": '''def min_distance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # delete
                    dp[i][j - 1],    # insert
                    dp[i - 1][j - 1] # replace
                )
    return dp[m][n]
''',
        "test": '''from tests.loader import load_exercise

min_distance = load_exercise("dynamic_programming/edit_distance.py", "min_distance")

def test_edit_dist():
    assert min_distance("horse", "ros") == 3
    assert min_distance("intention", "execution") == 5
''',
        "hints": {
            1: "dp[i][j] = min distance between word1[:i] and word2[:j].",
            2: "If match: dp[i][j] = dp[i-1][j-1].",
            3: "Else: 1 + min(insert, delete, replace).",
            4: "O(M * N) time.",
            5: "See reference in reference/dynamic_programming/edit_distance.py."
        }
    },
    {
        "id": "dp-2d-memo",
        "name": "Target Sum (2D Memoization)",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(N * Sum)",
        "space_complexity": "O(N * Sum)",
        "file": "target_sum_memo.py",
        "starter": '''def find_target_sum_ways(nums: list[int], target: int) -> int:
    """
    Assign '+' or '-' signs to each integer in nums such that the sum equals target.
    Target Time: O(N * Sum)
    Target Space: O(N * Sum)
    """
    raise NotImplementedError
''',
        "reference": '''def find_target_sum_ways(nums: list[int], target: int) -> int:
    memo = {}
    def dfs(i: int, current_sum: int) -> int:
        if i == len(nums):
            return 1 if current_sum == target else 0
        state = (i, current_sum)
        if state in memo:
            return memo[state]
        ways = dfs(i + 1, current_sum + nums[i]) + dfs(i + 1, current_sum - nums[i])
        memo[state] = ways
        return ways
    return dfs(0, 0)
''',
        "test": '''from tests.loader import load_exercise

find_target_sum_ways = load_exercise("dynamic_programming/target_sum_memo.py", "find_target_sum_ways")

def test_target_sum():
    assert find_target_sum_ways([1, 1, 1, 1, 1], 3) == 5
    assert find_target_sum_ways([1], 1) == 1
''',
        "hints": {
            1: "State tuple is (index, current_sum).",
            2: "Recurse adding nums[i] and subtracting nums[i].",
            3: "Memoize results in dictionary.",
            4: "Base case: i == len(nums) checks current_sum == target.",
            5: "See reference in reference/dynamic_programming/target_sum_memo.py."
        }
    },
    {
        "id": "dp-take-or-skip",
        "name": "Take or Skip Recursion (Subset Sum)",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N * target)",
        "space_complexity": "O(N * target)",
        "file": "take_or_skip.py",
        "starter": '''def can_partition_sum(nums: list[int], target: int) -> bool:
    """
    Determine whether there exists a subset of nums summing exactly to target.
    Target Time: O(N * target)
    Target Space: O(N * target)
    """
    raise NotImplementedError
''',
        "reference": '''def can_partition_sum(nums: list[int], target: int) -> bool:
    memo = {}
    def dfs(i: int, remain: int) -> bool:
        if remain == 0:
            return True
        if i == len(nums) or remain < 0:
            return False
        state = (i, remain)
        if state in memo:
            return memo[state]
        # Take or skip
        ans = dfs(i + 1, remain - nums[i]) or dfs(i + 1, remain)
        memo[state] = ans
        return ans
    return dfs(0, target)
''',
        "test": '''from tests.loader import load_exercise

can_partition_sum = load_exercise("dynamic_programming/take_or_skip.py", "can_partition_sum")

def test_take_or_skip():
    assert can_partition_sum([1, 5, 11, 5], 11) is True
    assert can_partition_sum([1, 2, 3, 5], 50) is False
''',
        "hints": {
            1: "At each element i, branch into take (remain - nums[i]) or skip (remain).",
            2: "Memoize (i, remain).",
            3: "Base case remain == 0 returns True.",
            4: "Base case i == len(nums) returns False.",
            5: "See reference in reference/dynamic_programming/take_or_skip.py."
        }
    },
    {
        "id": "dp-bottom-up-tab",
        "name": "Partition Equal Subset Sum (Tabulation)",
        "category": "dynamic_programming",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(N * Sum)",
        "space_complexity": "O(Sum)",
        "file": "partition_subset_sum.py",
        "starter": '''def can_partition(nums: list[int]) -> bool:
    """
    Determine if array can be partitioned into two subsets with equal sums.
    Target Time: O(N * Sum)
    Target Space: O(Sum)
    """
    raise NotImplementedError
''',
        "reference": '''def can_partition(nums: list[int]) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False
    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True
    for x in nums:
        for s in range(target, x - 1, -1):
            dp[s] = dp[s] or dp[s - x]
    return dp[target]
''',
        "test": '''from tests.loader import load_exercise

can_partition = load_exercise("dynamic_programming/partition_subset_sum.py", "can_partition")

def test_partition():
    assert can_partition([1, 5, 11, 5]) is True
    assert can_partition([1, 2, 3, 5]) is False
''',
        "hints": {
            1: "Sum must be even, target = total // 2.",
            2: "Boolean array dp where dp[s] indicates if sum s is achievable.",
            3: "Iterate s backwards from target down to x.",
            4: "O(target) auxiliary space.",
            5: "See reference in reference/dynamic_programming/partition_subset_sum.py."
        }
    },
    {
        "id": "dp-space-optimized",
        "name": "Maximum Subarray (Kadane's Space-Optimized)",
        "category": "dynamic_programming",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "max_subarray.py",
        "starter": '''def max_sub_array(nums: list[int]) -> int:
    """
    Find contiguous subarray with largest sum (Kadane's algorithm).
    Target Time: O(N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''def max_sub_array(nums: list[int]) -> int:
    if not nums:
        return 0
    max_so_far = nums[0]
    curr_max = nums[0]
    for x in nums[1:]:
        curr_max = max(x, curr_max + x)
        max_so_far = max(max_so_far, curr_max)
    return max_so_far
''',
        "test": '''from tests.loader import load_exercise

max_sub_array = load_exercise("dynamic_programming/max_subarray.py", "max_sub_array")

def test_kadane():
    assert max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6
    assert max_sub_array([1]) == 1
    assert max_sub_array([5, 4, -1, 7, 8]) == 23
''',
        "hints": {
            1: "curr_max = max(x, curr_max + x).",
            2: "Either start a new subarray at x or extend previous.",
            3: "Track overall maximum max_so_far.",
            4: "O(N) time and O(1) space.",
            5: "See reference in reference/dynamic_programming/max_subarray.py."
        }
    }
]
