from tests.loader import load_exercise

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
