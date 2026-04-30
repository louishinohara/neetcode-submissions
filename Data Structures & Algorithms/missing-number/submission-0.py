class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        # Sum of all - n factorial thing
        total = 0
        for i in range(len(nums) + 1):
            total += i
        return total - sum(nums)