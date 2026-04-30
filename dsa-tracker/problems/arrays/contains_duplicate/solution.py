"""
Contains Duplicate
Difficulty: easy
Topic: arrays
Pattern(s): hashing

See notes.md in this directory for analysis.
"""


class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        # O(n) time, O(n) space — single-pass hash set lookup beats the
        # O(n^2) pairwise check and the O(n log n) sort-and-compare.
        seen: set[int] = set()
        for num in nums:
            if num in seen:
                return True
            seen.add(num)
        return False
