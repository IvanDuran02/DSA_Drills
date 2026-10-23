"""Backtracking algorithm definitions (8 exercises)"""

BACKTRACKING_EXERCISES = [
    {
        "id": "backtrack-subsets",
        "name": "Subsets (Power Set)",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N * 2^N)",
        "space_complexity": "O(N)",
        "file": "subsets.py",
        "starter": '''def subsets(nums: list[int]) -> list[list[int]]:
    """
    Return all possible subsets (power set) of distinct integers nums.
    Target Time: O(N * 2^N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def subsets(nums: list[int]) -> list[list[int]]:
    res = []
    subset = []
    def backtrack(start: int):
        res.append(list(subset))
        for i in range(start, len(nums)):
            subset.append(nums[i])
            backtrack(i + 1)
            subset.pop()
    backtrack(0)
    return res
''',
        "test": '''from tests.loader import load_exercise

subsets = load_exercise("backtracking/subsets.py", "subsets")

def test_subsets():
    res = subsets([1, 2, 3])
    assert len(res) == 8
    assert [] in res
    assert [1, 2, 3] in res
''',
        "hints": {
            1: "At each step, append current copy of subset to result.",
            2: "Iterate from start index, append nums[i], recurse with i + 1, pop().",
            3: "Total subsets is 2^N.",
            4: "Backtrack pop() restores state.",
            5: "See reference in reference/backtracking/subsets.py."
        }
    },
    {
        "id": "backtrack-subsets-duplicates",
        "name": "Subsets II (With Duplicates)",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(N * 2^N)",
        "space_complexity": "O(N)",
        "file": "subsets_duplicates.py",
        "starter": '''def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    """
    Return all possible subsets with duplicate handling.
    Target Time: O(N * 2^N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def subsets_with_dup(nums: list[int]) -> list[list[int]]:
    nums.sort()
    res = []
    subset = []
    def backtrack(start: int):
        res.append(list(subset))
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            subset.append(nums[i])
            backtrack(i + 1)
            subset.pop()
    backtrack(0)
    return res
''',
        "test": '''from tests.loader import load_exercise

subsets_with_dup = load_exercise("backtracking/subsets_duplicates.py", "subsets_with_dup")

def test_subsets_dup():
    res = subsets_with_dup([1, 2, 2])
    assert len(res) == 6
''',
        "hints": {
            1: "Sort nums to group duplicates together.",
            2: "Skip duplicate elements: if i > start and nums[i] == nums[i - 1]: continue.",
            3: "This prevents duplicate subset branches at the same recursion depth.",
            4: "O(N * 2^N) time.",
            5: "See reference in reference/backtracking/subsets_duplicates.py."
        }
    },
    {
        "id": "backtrack-permutations",
        "name": "Permutations",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N * N!)",
        "space_complexity": "O(N)",
        "file": "permutations.py",
        "starter": '''def permute(nums: list[int]) -> list[list[int]]:
    """
    Return all possible permutations of array of distinct integers.
    Target Time: O(N * N!)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def permute(nums: list[int]) -> list[list[int]]:
    res = []
    used = [False] * len(nums)
    curr = []
    def backtrack():
        if len(curr) == len(nums):
            res.append(list(curr))
            return
        for i in range(len(nums)):
            if not used[i]:
                used[i] = True
                curr.append(nums[i])
                backtrack()
                curr.pop()
                used[i] = False
    backtrack()
    return res
''',
        "test": '''from tests.loader import load_exercise

permute = load_exercise("backtracking/permutations.py", "permute")

def test_permutations():
    res = permute([1, 2, 3])
    assert len(res) == 6
''',
        "hints": {
            1: "Maintain boolean array 'used' of length N.",
            2: "Base case: len(curr) == len(nums).",
            3: "Iterate all unused items, recurse, then unmark used and pop.",
            4: "Total permutations N!.",
            5: "See reference in reference/backtracking/permutations.py."
        }
    },
    {
        "id": "backtrack-combinations",
        "name": "Combinations (n choose k)",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(k * C(n, k))",
        "space_complexity": "O(k)",
        "file": "combinations.py",
        "starter": '''def combine(n: int, k: int) -> list[list[int]]:
    """
    Return all combinations of k numbers chosen from range 1 to n.
    Target Time: O(k * C(n, k))
    Target Space: O(k)
    """
    raise NotImplementedError
''',
        "reference": '''def combine(n: int, k: int) -> list[list[int]]:
    res = []
    comb = []
    def backtrack(start: int):
        if len(comb) == k:
            res.append(list(comb))
            return
        # Pruning: need (k - len(comb)) more elements
        needed = k - len(comb)
        for i in range(start, n - needed + 2):
            comb.append(i)
            backtrack(i + 1)
            comb.pop()
    backtrack(1)
    return res
''',
        "test": '''from tests.loader import load_exercise

combine = load_exercise("backtracking/combinations.py", "combine")

def test_combine():
    res = combine(4, 2)
    assert len(res) == 6
''',
        "hints": {
            1: "Base case: len(comb) == k.",
            2: "Recurse from start index to n.",
            3: "Prune loop range when remaining elements cannot satisfy needed count.",
            4: "Space is O(k).",
            5: "See reference in reference/backtracking/combinations.py."
        }
    },
    {
        "id": "backtrack-combination-sum",
        "name": "Combination Sum",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 12,
        "time_complexity": "O(N^(T/M))",
        "space_complexity": "O(T/M)",
        "file": "combination_sum.py",
        "starter": '''def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    """
    Find all unique combinations of candidates where numbers sum to target.
    Same number may be chosen unlimited number of times.
    Target Time: O(N^(T/M))
    Target Space: O(T/M)
    """
    raise NotImplementedError
''',
        "reference": '''def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    res = []
    candidates.sort()
    comb = []
    def backtrack(start: int, remain: int):
        if remain == 0:
            res.append(list(comb))
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break
            comb.append(candidates[i])
            backtrack(i, remain - candidates[i])
            comb.pop()
    backtrack(0, target)
    return res
''',
        "test": '''from tests.loader import load_exercise

combination_sum = load_exercise("backtracking/combination_sum.py", "combination_sum")

def test_comb_sum():
    res = combination_sum([2, 3, 6, 7], 7)
    assert [7] in res
    assert [2, 2, 3] in res
''',
        "hints": {
            1: "Pass current index i (not i + 1) to allow reusing same candidate.",
            2: "Sort candidates to break early when candidates[i] > remain.",
            3: "Base case remain == 0 adds combination.",
            4: "O(T/M) recursion depth where M is min candidate.",
            5: "See reference in reference/backtracking/combination_sum.py."
        }
    },
    {
        "id": "backtrack-palindrome-partitioning",
        "name": "Palindrome Partitioning",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(N * 2^N)",
        "space_complexity": "O(N)",
        "file": "palindrome_partition.py",
        "starter": '''def partition(s: str) -> list[list[str]]:
    """
    Partition string s such that every substring in the partition is a palindrome.
    Target Time: O(N * 2^N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def partition(s: str) -> list[list[str]]:
    res = []
    path = []
    def is_palindrome(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start: int):
        if start == len(s):
            res.append(list(path))
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if is_palindrome(sub):
                path.append(sub)
                backtrack(end)
                path.pop()
    backtrack(0)
    return res
''',
        "test": '''from tests.loader import load_exercise

partition = load_exercise("backtracking/palindrome_partition.py", "partition")

def test_partition():
    res = partition("aab")
    assert sorted(res) == sorted([["a", "a", "b"], ["aa", "b"]])
''',
        "hints": {
            1: "Try every prefix s[start:end].",
            2: "If prefix is palindrome, append to path and recurse with end.",
            3: "Base case is start == len(s).",
            4: "O(N * 2^N) time.",
            5: "See reference in reference/backtracking/palindrome_partition.py."
        }
    },
    {
        "id": "backtrack-word-search",
        "name": "Word Search in Grid",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(N * 3^L)",
        "space_complexity": "O(L)",
        "file": "word_search.py",
        "starter": '''def exist(board: list[list[str]], word: str) -> bool:
    """
    Determine if word exists in grid with horizontally or vertically adjacent cells.
    Target Time: O(N * 3^L)
    Target Space: O(L)
    """
    raise NotImplementedError
''',
        "reference": '''def exist(board: list[list[str]], word: str) -> bool:
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])

    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols and board[r][c] == word[idx]):
            return False

        temp = board[r][c]
        board[r][c] = "#"  # mark visited

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if backtrack(r + dr, c + dc, idx + 1):
                board[r][c] = temp
                return True

        board[r][c] = temp  # restore
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if backtrack(r, c, 0):
                    return True
    return False
''',
        "test": '''from tests.loader import load_exercise

exist = load_exercise("backtracking/word_search.py", "exist")

def test_word_search():
    board = [
        ["A", "B", "C", "E"],
        ["S", "F", "C", "S"],
        ["A", "D", "E", "E"]
    ]
    assert exist(board, "ABCCED") is True
    assert exist(board, "SEE") is True
    assert exist(board, "ABCB") is False
''',
        "hints": {
            1: "Temporarily replace board[r][c] with '#' to mark visited without extra memory.",
            2: "Restore character board[r][c] = temp before returning.",
            3: "Check 4 neighbors: (0, 1), (1, 0), (0, -1), (-1, 0).",
            4: "Base case idx == len(word) indicates success.",
            5: "See reference in reference/backtracking/word_search.py."
        }
    },
    {
        "id": "backtrack-generate-parentheses",
        "name": "Generate Valid Parentheses",
        "category": "backtracking",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(4^N / sqrt(N))",
        "space_complexity": "O(N)",
        "file": "generate_parentheses.py",
        "starter": '''def generate_parenthesis(n: int) -> list[str]:
    """
    Generate all combinations of well-formed parentheses of length 2n.
    Target Time: O(4^N / sqrt(N)) (Catalan number)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def generate_parenthesis(n: int) -> list[str]:
    res = []
    curr = []
    def backtrack(open_count: int, close_count: int):
        if len(curr) == 2 * n:
            res.append("".join(curr))
            return
        if open_count < n:
            curr.append("(")
            backtrack(open_count + 1, close_count)
            curr.pop()
        if close_count < open_count:
            curr.append(")")
            backtrack(open_count, close_count + 1)
            curr.pop()
    backtrack(0, 0)
    return res
''',
        "test": '''from tests.loader import load_exercise

generate_parenthesis = load_exercise("backtracking/generate_parentheses.py", "generate_parenthesis")

def test_gen_parens():
    res = generate_parenthesis(3)
    assert len(res) == 5
    assert "((()))" in res
    assert "()()()" in res
''',
        "hints": {
            1: "Can add '(' if open_count < n.",
            2: "Can add ')' if close_count < open_count.",
            3: "Base case len(curr) == 2 * n.",
            4: "Catalan number count: C_n = (2n)! / ((n+1)! * n!).",
            5: "See reference in reference/backtracking/generate_parentheses.py."
        }
    }
]
