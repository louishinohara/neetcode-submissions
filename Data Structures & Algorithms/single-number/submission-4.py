class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        k = {}

        for num in nums:
            if num in k:
                k[num] += 1
            else:
                k[num] = 1
        
        for i in k.keys():
            if k[i] == 1:
                return i