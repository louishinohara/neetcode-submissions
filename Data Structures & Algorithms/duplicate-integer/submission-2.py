class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        map = {}

        for num in nums:
            if num not in map:
                map[num] = 1
            else:
                return True
        return False