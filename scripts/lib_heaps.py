"""Heap algorithm definitions (10 exercises) supporting Python 3.14 native max-heaps"""

HEAP_EXERCISES = [
    {
        "id": "heap-native-min",
        "name": "Native Min-Heap Operations",
        "category": "heaps",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(log N)",
        "space_complexity": "O(N)",
        "file": "native_min_heap.py",
        "starter": '''import heapq

class MinHeapPractice:
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError
''',
        "reference": '''import heapq

class MinHeapPractice:
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        heapq.heappush(self.heap, val)

    def pop(self) -> int:
        return heapq.heappop(self.heap)

    def peek(self) -> int:
        return self.heap[0]
''',
        "test": '''from tests.loader import load_exercise

MinHeapPractice = load_exercise("heaps/native_min_heap.py", "MinHeapPractice")

def test_min_heap():
    h = MinHeapPractice()
    h.push(5)
    h.push(2)
    h.push(8)
    assert h.peek() == 2
    assert h.pop() == 2
    assert h.pop() == 5
    assert h.pop() == 8
''',
        "hints": {
            1: "Use heapq.heappush(self.heap, val).",
            2: "Use heapq.heappop(self.heap).",
            3: "Smallest element is at self.heap[0].",
            4: "All push and pop operations take O(log N).",
            5: "See reference in reference/heaps/native_min_heap.py."
        }
    },
    {
        "id": "heap-native-max",
        "name": "Native Python 3.14 Max-Heap Operations",
        "category": "heaps",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(log N)",
        "space_complexity": "O(N)",
        "file": "native_max_heap.py",
        "starter": '''import heapq

class MaxHeapPractice:
    """
    Max-heap using Python 3.14 native heapq max-heap functions:
    heapq.heappush_max, heapq.heappop_max
    """
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError
''',
        "reference": '''import heapq

class MaxHeapPractice:
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        heapq.heappush_max(self.heap, val)

    def pop(self) -> int:
        return heapq.heappop_max(self.heap)

    def peek(self) -> int:
        return self.heap[0]
''',
        "test": '''from tests.loader import load_exercise
import heapq

MaxHeapPractice = load_exercise("heaps/native_max_heap.py", "MaxHeapPractice")

def test_max_heap():
    h = MaxHeapPractice()
    h.push(3)
    h.push(10)
    h.push(5)
    assert h.peek() == 10
    assert h.pop() == 10
    assert h.pop() == 5
    assert h.pop() == 3
''',
        "hints": {
            1: "Python 3.14 native max-heap uses heapq.heappush_max(self.heap, val).",
            2: "Pop max element with heapq.heappop_max(self.heap).",
            3: "Largest element resides at index 0.",
            4: "No negative number negation needed in Python 3.14+.",
            5: "See reference in reference/heaps/native_max_heap.py."
        }
    },
    {
        "id": "heap-construction",
        "name": "Heap Construction (Linear Heapify)",
        "category": "heaps",
        "difficulty": "Easy",
        "level": 2,
        "recommended_minutes": 8,
        "time_complexity": "O(N)",
        "space_complexity": "O(1)",
        "file": "heap_construction.py",
        "starter": '''import heapq

def build_min_and_max_heaps(nums: list[int]) -> tuple[list[int], list[int]]:
    """
    Build in-place min-heap and max-heap using Python 3.14 heapify functions.
    Returns (min_heap, max_heap).
    Target Time: O(N)
    Target Space: O(N)
    """
    raise NotImplementedError
''',
        "reference": '''import heapq

def build_min_and_max_heaps(nums: list[int]) -> tuple[list[int], list[int]]:
    min_h = list(nums)
    max_h = list(nums)
    heapq.heapify(min_h)
    heapq.heapify_max(max_h)
    return min_h, max_h
''',
        "test": '''from tests.loader import load_exercise

build_min_and_max_heaps = load_exercise("heaps/heap_construction.py", "build_min_and_max_heaps")

def test_construction():
    nums = [9, 3, 7, 1, 5, 2]
    min_h, max_h = build_min_and_max_heaps(nums)
    assert min_h[0] == 1
    assert max_h[0] == 9
''',
        "hints": {
            1: "heapq.heapify(list) transforms list into min-heap in O(N).",
            2: "heapq.heapify_max(list) transforms list into max-heap in O(N) in Python 3.14.",
            3: "Copy list before heapifying if original list must be preserved.",
            4: "Linear time O(N) is faster than N successive pushes O(N log N).",
            5: "See reference in reference/heaps/heap_construction.py."
        }
    },
    {
        "id": "heap-push-pop-replace",
        "name": "Heap Replacement Operations",
        "category": "heaps",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "file": "heap_replace.py",
        "starter": '''import heapq

def replace_min_and_max(min_heap: list[int], max_heap: list[int], val: int) -> tuple[int, int]:
    """
    Perform heapreplace on min_heap and heapreplace_max on max_heap with val.
    Returns (popped_min, popped_max).
    Target Time: O(log N)
    Target Space: O(1)
    """
    raise NotImplementedError
''',
        "reference": '''import heapq

def replace_min_and_max(min_heap: list[int], max_heap: list[int], val: int) -> tuple[int, int]:
    popped_min = heapq.heapreplace(min_heap, val)
    popped_max = heapq.heapreplace_max(max_heap, val)
    return popped_min, popped_max
''',
        "test": '''from tests.loader import load_exercise
import heapq

replace_min_and_max = load_exercise("heaps/heap_replace.py", "replace_min_and_max")

def test_replacement():
    min_h = [1, 3, 5]
    max_h = [10, 8, 6]
    heapq.heapify(min_h)
    heapq.heapify_max(max_h)
    p_min, p_max = replace_min_and_max(min_h, max_h, 7)
    assert p_min == 1
    assert p_max == 10
    assert min_h[0] == 3
    assert max_h[0] == 8
''',
        "hints": {
            1: "heapreplace pops and returns current root, then inserts new item.",
            2: "heapreplace_max performs the same replacement on a max-heap in Python 3.14.",
            3: "Single sift-down is more efficient than a separate heappop followed by heappush.",
            4: "O(log N) time.",
            5: "See reference in reference/heaps/heap_replace.py."
        }
    },
    {
        "id": "heap-kth-largest",
        "name": "Kth Largest Element in an Array",
        "category": "heaps",
        "difficulty": "Medium",
        "level": 2,
        "recommended_minutes": 10,
        "time_complexity": "O(N log K)",
        "space_complexity": "O(K)",
        "file": "kth_largest.py",
        "starter": '''import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    """
    Find kth largest element in unsorted array using a min-heap of size k.
    Target Time: O(N log K)
    Target Space: O(K)
    """
    raise NotImplementedError
''',
        "reference": '''import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
''',
        "test": '''from tests.loader import load_exercise

find_kth_largest = load_exercise("heaps/kth_largest.py", "find_kth_largest")

def test_kth():
    assert find_kth_largest([3, 2, 1, 5, 6, 4], 2) == 5
    assert find_kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4) == 4
''',
        "hints": {
            1: "A min-heap of size K keeps the K largest elements seen so far.",
            2: "The smallest of the K largest elements is the root heap[0].",
            3: "Push onto heap, and pop whenever size exceeds K.",
            4: "Time complexity O(N log K), space O(K).",
            5: "See reference in reference/heaps/kth_largest.py."
        }
    },
    {
        "id": "heap-top-k-frequent",
        "name": "Top K Frequent Elements",
        "category": "heaps",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(N log K)",
        "space_complexity": "O(N + K)",
        "file": "top_k_frequent.py",
        "starter": '''import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    """
    Return the k most frequent elements in nums.
    Target Time: O(N log K)
    Target Space: O(N + K)
    """
    raise NotImplementedError
''',
        "reference": '''import heapq
from collections import Counter

def top_k_frequent(nums: list[int], k: int) -> list[int]:
    count = Counter(nums)
    heap = []
    for num, freq in count.items():
        heapq.heappush(heap, (freq, num))
        if len(heap) > k:
            heapq.heappop(heap)
    return [num for freq, num in heap]
''',
        "test": '''from tests.loader import load_exercise

top_k_frequent = load_exercise("heaps/top_k_frequent.py", "top_k_frequent")

def test_top_k():
    res = top_k_frequent([1, 1, 1, 2, 2, 3], 2)
    assert set(res) == {1, 2}
''',
        "hints": {
            1: "Count frequencies with Counter(nums).",
            2: "Maintain min-heap of (freq, num) tuples with max size k.",
            3: "Pop when size exceeds k to retain k most frequent.",
            4: "O(N log K) time.",
            5: "See reference in reference/heaps/top_k_frequent.py."
        }
    },
    {
        "id": "heap-merge-k-sorted",
        "name": "Merge K Sorted Lists",
        "category": "heaps",
        "difficulty": "Hard",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(N log K)",
        "space_complexity": "O(K)",
        "file": "merge_k_sorted.py",
        "starter": '''import heapq

def merge_k_sorted_arrays(arrays: list[list[int]]) -> list[int]:
    """
    Merge k sorted integer arrays into one sorted array using a min-heap.
    Target Time: O(N log K)
    Target Space: O(K)
    """
    raise NotImplementedError
''',
        "reference": '''import heapq

def merge_k_sorted_arrays(arrays: list[list[int]]) -> list[int]:
    heap = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(heap, (arr[0], i, 0))

    result = []
    while heap:
        val, arr_idx, elem_idx = heapq.heappop(heap)
        result.append(val)
        if elem_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][elem_idx + 1]
            heapq.heappush(heap, (next_val, arr_idx, elem_idx + 1))

    return result
''',
        "test": '''from tests.loader import load_exercise

merge_k_sorted_arrays = load_exercise("heaps/merge_k_sorted.py", "merge_k_sorted_arrays")

def test_merge_k():
    arrays = [[1, 4, 5], [1, 3, 4], [2, 6]]
    res = merge_k_sorted_arrays(arrays)
    assert res == [1, 1, 2, 3, 4, 4, 5, 6]
''',
        "hints": {
            1: "Heap holds current front element from each of the K lists: (val, list_index, elem_index).",
            2: "Pop minimum element, append to result, push next element from that same list.",
            3: "Heap size never exceeds K.",
            4: "O(N log K) where N is total elements across all lists.",
            5: "See reference in reference/heaps/merge_k_sorted.py."
        }
    },
    {
        "id": "heap-median-stream",
        "name": "Find Median from Data Stream (Two Heaps)",
        "category": "heaps",
        "difficulty": "Hard",
        "level": 3,
        "recommended_minutes": 15,
        "time_complexity": "O(log N) add, O(1) find",
        "space_complexity": "O(N)",
        "file": "median_stream.py",
        "starter": '''import heapq

class MedianFinder:
    """
    Find median from streaming numbers using Python 3.14 native max-heap for lower half
    and standard min-heap for upper half.
    """
    def __init__(self):
        raise NotImplementedError

    def add_num(self, num: int) -> None:
        raise NotImplementedError

    def find_median(self) -> float:
        raise NotImplementedError
''',
        "reference": '''import heapq

class MedianFinder:
    def __init__(self):
        self.max_heap: list[int] = []  # lower half (Python 3.14 native max-heap)
        self.min_heap: list[int] = []  # upper half (min-heap)

    def add_num(self, num: int) -> None:
        if not self.max_heap or num <= self.max_heap[0]:
            heapq.heappush_max(self.max_heap, num)
        else:
            heapq.heappush(self.min_heap, num)

        # Balance sizes so max_heap has either same count or 1 more than min_heap
        if len(self.max_heap) > len(self.min_heap) + 1:
            val = heapq.heappop_max(self.max_heap)
            heapq.heappush(self.min_heap, val)
        elif len(self.min_heap) > len(self.max_heap):
            val = heapq.heappop(self.min_heap)
            heapq.heappush_max(self.max_heap, val)

    def find_median(self) -> float:
        if len(self.max_heap) > len(self.min_heap):
            return float(self.max_heap[0])
        return (self.max_heap[0] + self.min_heap[0]) / 2.0
''',
        "test": '''from tests.loader import load_exercise

MedianFinder = load_exercise("heaps/median_stream.py", "MedianFinder")

def test_median():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0
''',
        "hints": {
            1: "Use Python 3.14 native heapq.heappush_max / heappop_max for the lower half.",
            2: "Use standard heapq min-heap for the upper half.",
            3: "Balance sizes such that len(max_heap) == len(min_heap) or len(max_heap) == len(min_heap) + 1.",
            4: "add_num runs in O(log N), find_median runs in O(1).",
            5: "See reference in reference/heaps/median_stream.py."
        }
    },
    {
        "id": "heap-priority-queue",
        "name": "Task Priority Queue with Removals",
        "category": "heaps",
        "difficulty": "Medium",
        "level": 3,
        "recommended_minutes": 12,
        "time_complexity": "O(log N)",
        "space_complexity": "O(N)",
        "file": "priority_queue.py",
        "starter": '''import heapq

class TaskPriorityQueue:
    def __init__(self):
        raise NotImplementedError

    def add_task(self, task_name: str, priority: int) -> None:
        raise NotImplementedError

    def remove_task(self, task_name: str) -> None:
        raise NotImplementedError

    def pop_highest_priority(self) -> str:
        raise NotImplementedError
''',
        "reference": '''import heapq

class TaskPriorityQueue:
    def __init__(self):
        self.pq = []
        self.entry_finder = {}
        self.REMOVED = '<removed>'

    def add_task(self, task_name: str, priority: int) -> None:
        if task_name in self.entry_finder:
            self.remove_task(task_name)
        entry = [-priority, task_name]
        self.entry_finder[task_name] = entry
        heapq.heappush(self.pq, entry)

    def remove_task(self, task_name: str) -> None:
        entry = self.entry_finder.pop(task_name, None)
        if entry:
            entry[-1] = self.REMOVED

    def pop_highest_priority(self) -> str:
        while self.pq:
            priority, task = heapq.heappop(self.pq)
            if task != self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')
''',
        "test": '''from tests.loader import load_exercise

TaskPriorityQueue = load_exercise("heaps/priority_queue.py", "TaskPriorityQueue")

def test_pq():
    pq = TaskPriorityQueue()
    pq.add_task("task1", 10)
    pq.add_task("task2", 20)
    pq.add_task("task3", 15)
    pq.remove_task("task2")
    assert pq.pop_highest_priority() == "task3"
    assert pq.pop_highest_priority() == "task1"
''',
        "hints": {
            1: "Maintain entry_finder dict mapping task -> mutable entry list [priority, task].",
            2: "To remove, mark entry[-1] = REMOVED sentinel and delete from entry_finder.",
            3: "Discard REMOVED entries lazily upon popping.",
            4: "O(log N) amortized operations.",
            5: "See reference in reference/heaps/priority_queue.py."
        }
    },
    {
        "id": "heap-legacy-negated-max",
        "name": "Legacy Negated-Value Max-Heap Pattern",
        "category": "heaps",
        "difficulty": "Easy",
        "level": 1,
        "recommended_minutes": 8,
        "time_complexity": "O(log N)",
        "space_complexity": "O(N)",
        "file": "legacy_negated_heap.py",
        "starter": '''import heapq

class LegacyMaxHeap:
    """
    Max-heap implemented using value negation for Python < 3.14 compatibility.
    """
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError
''',
        "reference": '''import heapq

class LegacyMaxHeap:
    def __init__(self):
        self.heap: list[int] = []

    def push(self, val: int) -> None:
        heapq.heappush(self.heap, -val)

    def pop(self) -> int:
        return -heapq.heappop(self.heap)

    def peek(self) -> int:
        return -self.heap[0]
''',
        "test": '''from tests.loader import load_exercise

LegacyMaxHeap = load_exercise("heaps/legacy_negated_heap.py", "LegacyMaxHeap")

def test_legacy():
    h = LegacyMaxHeap()
    h.push(10)
    h.push(30)
    h.push(20)
    assert h.peek() == 30
    assert h.pop() == 30
    assert h.pop() == 20
    assert h.pop() == 10
''',
        "hints": {
            1: "Store -val in standard min-heap.",
            2: "Negate again upon popping: -heappop().",
            3: "Legacy pattern used prior to Python 3.14 native max-heap APIs.",
            4: "O(log N) operations.",
            5: "See reference in reference/heaps/legacy_negated_heap.py."
        }
    }
]
