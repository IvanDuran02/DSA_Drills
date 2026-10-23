def search_range(nums: list[int], target: int) -> list[int]:
    def find_first():
        l, r = 0, len(nums) - 1
        res = -1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                res = mid
                r = mid - 1
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return res

    def find_last():
        l, r = 0, len(nums) - 1
        res = -1
        while l <= r:
            mid = (l + r) // 2
            if nums[mid] == target:
                res = mid
                l = mid + 1
            elif nums[mid] < target:
                l = mid + 1
            else:
                r = mid - 1
        return res

    return [find_first(), find_last()]
