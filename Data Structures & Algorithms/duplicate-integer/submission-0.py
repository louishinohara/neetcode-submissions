class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        # Solution 1: Put into hashmap and check for any greater than 1
        # Solution 2: Sort and check i + 1
        hashMap = {}
        for num in nums:
            if num not in hashMap:
                hashMap[num] = 1
            else:
                hashMap[num] += 1
            if hashMap[num] > 1:
                return True
        return False