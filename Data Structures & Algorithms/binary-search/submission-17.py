class Solution:
    def search(self, nums: List[int], target: int) -> int:
        
        # Require base case
        def helper(l, r):
            if l > r:
                return -1
            else:
                mid = (l + r) // 2
                print(l,r,mid)
                if nums[mid] == target:
                    return mid
                elif nums[mid] < target:
                    return helper(mid + 1, r)
                else: 
                    return helper(l, mid-1)

        # Require return
        return helper(0, len(nums) - 1)