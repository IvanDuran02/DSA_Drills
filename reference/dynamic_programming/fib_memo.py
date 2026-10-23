def fib_memo(n: int) -> int:
    memo = {0: 0, 1: 1}
    def helper(k: int) -> int:
        if k not in memo:
            memo[k] = helper(k - 1) + helper(k - 2)
        return memo[k]
    return helper(n)
