"""Stack algorithm definitions (6 exercises)"""

STACK_EXERCISES = [
    {
        "id": "stack-basic-ops",
        "name": "Basic Stack Operations",
        "category": "stacks",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 6,
        "time_complexity": "O(1) per op",
        "space_complexity": "O(N)",
        "file": "basic_stack.py",
        "starter": '''class ArrayStack:
    def __init__(self):
        self._items = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError
''',
        "reference": '''class ArrayStack:
    def __init__(self):
        self._items = []

    def push(self, val: int) -> None:
        self._items.append(val)

    def pop(self) -> int:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> int:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0
''',
        "test": '''from tests.loader import load_exercise
import pytest

ArrayStack = load_exercise("stacks/basic_stack.py", "ArrayStack")

def test_stack_ops():
    s = ArrayStack()
    assert s.is_empty() is True
    s.push(10)
    s.push(20)
    assert s.peek() == 20
    assert s.pop() == 20
    assert s.pop() == 10
    assert s.is_empty() is True
''',
        "hints": {
            1: "Use list.append and list.pop for O(1) amortized stack behavior.",
            2: "peek accesses self._items[-1].",
            3: "Raise IndexError if popping/peeking empty stack.",
            4: "O(1) time per operation.",
            5: "See reference in reference/stacks/basic_stack.py."
        }
    },
    {
        "id": "stack-valid-parentheses",
        "name": "Valid Parentheses",
        "category": "stacks",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "valid_parentheses.py",
        "starter": '''def is_valid(s: str) -> bool:
    """
    Determine if string s with characters '()[]{}' has valid brackets.
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def is_valid(s: str) -> bool:
    stack = []
    mapping = {')': '(', '}': '{', ']': '['}
    for char in s:
        if char in mapping:
            top = stack.pop() if stack else '#'
            if mapping[char] != top:
                return False
        else:
            stack.append(char)
    return len(stack) == 0
''',
        "test": '''from tests.loader import load_exercise

is_valid = load_exercise("stacks/valid_parentheses.py", "is_valid")

def test_valid_parens():
    assert is_valid("()") is True
    assert is_valid("()[]{}") is True
    assert is_valid("(]") is False
    assert is_valid("([)]") is False
''',
        "hints": {
            1: "Push opening brackets onto stack.",
            2: "When closing bracket encountered, pop top and verify match.",
            3: "Check len(stack) == 0 at the end.",
            4: "O(N) time and O(N) space.",
            5: "See reference in reference/stacks/valid_parentheses.py."
        }
    },
    {
        "id": "stack-monotonic",
        "name": "Monotonic Stack (Previous Smaller Element)",
        "category": "stacks",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "monotonic_stack.py",
        "starter": '''def previous_smaller_element(nums: list[int]) -> list[int]:
    """
    For each element, find previous strictly smaller element's value.
    Return -1 if none exists.
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def previous_smaller_element(nums: list[int]) -> list[int]:
    res = [-1] * len(nums)
    stack = []  # increasing stack of values
    for i, x in enumerate(nums):
        while stack and stack[-1] >= x:
            stack.pop()
        if stack:
            res[i] = stack[-1]
        stack.append(x)
    return res
''',
        "test": '''from tests.loader import load_exercise

previous_smaller_element = load_exercise("stacks/monotonic_stack.py", "previous_smaller_element")

def test_prev_smaller():
    assert previous_smaller_element([4, 5, 2, 10, 8]) == [-1, 4, -1, 2, 2]
''',
        "hints": {
            1: "Maintain stack of strictly increasing elements.",
            2: "Pop while stack[-1] >= x.",
            3: "Top of stack is previous smaller; append x to stack.",
            4: "Each element pushed and popped once: O(N) time.",
            5: "See reference in reference/stacks/monotonic_stack.py."
        }
    },
    {
        "id": "stack-daily-temperatures",
        "name": "Daily Temperatures",
        "category": "stacks",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "daily_temperatures.py",
        "starter": '''def daily_temperatures(temperatures: list[int]) -> list[int]:
    """
    For each day, find number of days until a warmer temperature.
    Return 0 if no future day is warmer.
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def daily_temperatures(temperatures: list[int]) -> list[int]:
    n = len(temperatures)
    res = [0] * n
    stack = []  # stores indices with decreasing temperatures
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            prev_idx = stack.pop()
            res[prev_idx] = i - prev_idx
        stack.append(i)
    return res
''',
        "test": '''from tests.loader import load_exercise

daily_temperatures = load_exercise("stacks/daily_temperatures.py", "daily_temperatures")

def test_daily_temps():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
''',
        "hints": {
            1: "Stack stores indices.",
            2: "While current temp > temperatures[stack[-1]], pop and record distance i - prev_idx.",
            3: "Stack maintains decreasing temperature indices.",
            4: "O(N) time.",
            5: "See reference in reference/stacks/daily_temperatures.py."
        }
    },
    {
        "id": "stack-next-greater",
        "name": "Next Greater Element",
        "category": "stacks",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "file": "next_greater_elem.py",
        "starter": '''def next_greater_elements(nums: list[int]) -> list[int]:
    """
    Find next greater element for each number in circular array nums.
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''def next_greater_elements(nums: list[int]) -> list[int]:
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
''',
        "test": '''from tests.loader import load_exercise

next_greater_elements = load_exercise("stacks/next_greater_elem.py", "next_greater_elements")

def test_next_greater():
    assert next_greater_elements([1, 2, 1]) == [2, -1, 2]
    assert next_greater_elements([1, 2, 3, 4, 3]) == [2, 3, 4, -1, 4]
''',
        "hints": {
            1: "Simulate circular array by iterating 2 * n times with index i % n.",
            2: "Push indices onto stack during first pass (i < n).",
            3: "Pop when nums[i % n] > nums[stack[-1]].",
            4: "O(N) time.",
            5: "See reference in reference/stacks/next_greater_elem.py."
        }
    },
    {
        "id": "stack-min-stack",
        "name": "Min Stack",
        "category": "stacks",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(1) all ops",
        "space_complexity": "O(N)",
        "file": "min_stack.py",
        "starter": '''class MinStack:
    """
    Stack supporting push, pop, top, and retrieving minimum element in O(1) time.
    """
    def __init__(self):
        raise NotImplementedError

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> None:
        raise NotImplementedError

    def top(self) -> int:
        raise NotImplementedError

    def get_min(self) -> int:
        raise NotImplementedError
''',
        "reference": '''class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        if not self.min_stack or val <= self.min_stack[-1]:
            self.min_stack.append(val)

    def pop(self) -> None:
        val = self.stack.pop()
        if val == self.min_stack[-1]:
            self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def get_min(self) -> int:
        return self.min_stack[-1]
''',
        "test": '''from tests.loader import load_exercise

MinStack = load_exercise("stacks/min_stack.py", "MinStack")

def test_min_stack():
    s = MinStack()
    s.push(-2)
    s.push(0)
    s.push(-3)
    assert s.get_min() == -3
    s.pop()
    assert s.top() == 0
    assert s.get_min() == -2
''',
        "hints": {
            1: "Use auxiliary min_stack tracking current minimums.",
            2: "Push to min_stack if empty or val <= min_stack[-1].",
            3: "Pop from min_stack if popped value == min_stack[-1].",
            4: "All operations O(1).",
            5: "See reference in reference/stacks/min_stack.py."
        }
    }
]
