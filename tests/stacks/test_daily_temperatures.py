from tests.loader import load_exercise

daily_temperatures = load_exercise("stacks/daily_temperatures.py", "daily_temperatures")

def test_daily_temps():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
