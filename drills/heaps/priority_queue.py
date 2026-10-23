import heapq

class TaskPriorityQueue:
    def __init__(self):
        raise NotImplementedError

    def add_task(self, task_name: str, priority: int) -> None:
        raise NotImplementedError

    def remove_task(self, task_name: str) -> None:
        raise NotImplementedError

    def pop_highest_priority(self) -> str:
        raise NotImplementedError
