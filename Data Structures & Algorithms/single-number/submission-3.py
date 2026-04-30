class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        
        def helper(i):           
            if i == len(nums) - 1:
                return nums[i]
            return nums[i] ^ helper(i + 1)

        return helper(0)

        