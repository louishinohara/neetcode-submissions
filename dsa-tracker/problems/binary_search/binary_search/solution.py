"""
Binary Search
Difficulty: easy
Topic: binary_search
Pattern(s): binary search

See notes.md in this directory for analysis.
"""


class Solution:
    def search(self, nums: list[int], target: int) -> int:
        # Iterative — preferred in Python (no TCO, lower constant factor).
        lo, hi = 0, len(nums) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1


class SolutionRecursive:
    def search(self, nums: list[int], target: int) -> int:
        def helper(l: int, r: int) -> int:
            if l > r:
                return -1
            mid = (l + r) // 2
            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                return helper(mid + 1, r)
            else:
                return helper(l, mid - 1)

        return helper(0, len(nums) - 1)
