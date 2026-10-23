from tests.loader import load_exercise

TaskPriorityQueue = load_exercise("heaps/priority_queue.py", "TaskPriorityQueue")

def test_pq():
    pq = TaskPriorityQueue()
    pq.add_task("task1", 10)
    pq.add_task("task2", 20)
    pq.add_task("task3", 15)
    pq.remove_task("task2")
    assert pq.pop_highest_priority() == "task3"
    assert pq.pop_highest_priority() == "task1"
