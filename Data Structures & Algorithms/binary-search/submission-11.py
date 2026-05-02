class Solution:
    def search(self, nums: List[int], target: int) -> int:
        
        # Require base case
        def helper(l, r):
            if l > r:
                return -1
            else:
                mid = (l + r) // 2
                if nums[mid] == target:
                    return mid
                elif mid < target:
                    return helper(mid + 1, r)
                else: 
                    return helper(l, r - 1)

        # Require return
        return helper(0, len(nums) - 1)