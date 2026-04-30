class Solution:
    def singleNumber(self, nums: List[int]) -> int:
        # Use map to keep track

        hmap = {}
        for num in nums:
            if num not in hmap:
                hmap[num] = 1
            else:
                hmap[num] += 1
        
        for k, v in hmap.items():
            if v == 1:
                return k
        
        return -1