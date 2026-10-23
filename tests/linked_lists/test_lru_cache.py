from tests.loader import load_exercise

LRUCache = load_exercise("linked_lists/lru_cache.py", "LRUCache")

def test_lru():
    cache = LRUCache(2)
    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1
    cache.put(3, 3)  # evicts 2
    assert cache.get(2) == -1
    cache.put(4, 4)  # evicts 1
    assert cache.get(1) == -1
    assert cache.get(3) == 3
    assert cache.get(4) == 4
