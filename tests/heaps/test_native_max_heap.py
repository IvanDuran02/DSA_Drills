from tests.loader import load_exercise
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
