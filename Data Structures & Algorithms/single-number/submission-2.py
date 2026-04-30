class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        
        def helper(i, acc):            
            if i == len(nums):
                return acc
            return helper(i + 1, acc ^ nums[i])

        return helper(1, nums[0])

        