from tests.loader import load_exercise

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
