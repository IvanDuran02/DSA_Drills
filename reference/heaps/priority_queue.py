import heapq

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
