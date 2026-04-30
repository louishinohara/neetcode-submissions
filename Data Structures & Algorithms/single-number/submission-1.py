class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        acc = nums[0]
        for i in range(1, len(nums)):
            acc ^= nums[i]
        return acc

        