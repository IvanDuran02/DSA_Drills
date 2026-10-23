class ArrayStack:
    def __init__(self):
        self._items = []

    def push(self, val: int) -> None:
        self._items.append(val)

    def pop(self) -> int:
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self) -> int:
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self) -> bool:
        return len(self._items) == 0
