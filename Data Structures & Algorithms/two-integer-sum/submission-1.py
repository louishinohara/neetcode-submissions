class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        # Brute force, check each item by iterating one at a time On^2
        # Two pointer, sort and then start from front and end til we reach target ONlog(N) + N = NLOGN
            # Can't do this because need ro return original index

        h = {}
        for i in range(len(nums)):
            diff = target - nums[i]
            if diff in h:
                return [h[diff], i]
            else:
                h[nums[i]] = i