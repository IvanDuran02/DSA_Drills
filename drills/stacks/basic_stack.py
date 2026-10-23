class ArrayStack:
    def __init__(self):
        self._items = []

    def push(self, val: int) -> None:
        raise NotImplementedError

    def pop(self) -> int:
        raise NotImplementedError

    def peek(self) -> int:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError
