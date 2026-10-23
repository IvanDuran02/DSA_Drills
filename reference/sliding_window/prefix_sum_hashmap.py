def subarray_sum(nums: list[int], k: int) -> int:
    prefix_counts = {0: 1}
    curr_sum = 0
    count = 0
    for x in nums:
        curr_sum += x
        diff = curr_sum - k
        if diff in prefix_counts:
            count += prefix_counts[diff]
        prefix_counts[curr_sum] = prefix_counts.get(curr_sum, 0) + 1
    return count
