from tests.loader import load_exercise

MedianFinder = load_exercise("heaps/median_stream.py", "MedianFinder")

def test_median():
    mf = MedianFinder()
    mf.add_num(1)
    mf.add_num(2)
    assert mf.find_median() == 1.5
    mf.add_num(3)
    assert mf.find_median() == 2.0
