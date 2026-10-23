def exist(board: list[list[str]], word: str) -> bool:
    if not board or not board[0]:
        return False
    rows, cols = len(board), len(board[0])

    def backtrack(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if not (0 <= r < rows and 0 <= c < cols and board[r][c] == word[idx]):
            return False

        temp = board[r][c]
        board[r][c] = "#"  # mark visited

        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if backtrack(r + dr, c + dc, idx + 1):
                board[r][c] = temp
                return True

        board[r][c] = temp  # restore
        return False

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == word[0]:
                if backtrack(r, c, 0):
                    return True
    return False
