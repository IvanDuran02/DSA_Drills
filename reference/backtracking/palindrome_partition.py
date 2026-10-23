def partition(s: str) -> list[list[str]]:
    res = []
    path = []
    def is_palindrome(sub: str) -> bool:
        return sub == sub[::-1]

    def backtrack(start: int):
        if start == len(s):
            res.append(list(path))
            return
        for end in range(start + 1, len(s) + 1):
            sub = s[start:end]
            if is_palindrome(sub):
                path.append(sub)
                backtrack(end)
                path.pop()
    backtrack(0)
    return res
