def generate_parenthesis(n: int) -> list[str]:
    res = []
    curr = []
    def backtrack(open_count: int, close_count: int):
        if len(curr) == 2 * n:
            res.append("".join(curr))
            return
        if open_count < n:
            curr.append("(")
            backtrack(open_count + 1, close_count)
            curr.pop()
        if close_count < open_count:
            curr.append(")")
            backtrack(open_count, close_count + 1)
            curr.pop()
    backtrack(0, 0)
    return res
