class Solution:
    def search(self, nums: List[int], target: int) -> int:
        
        def binSearch(i, j, nums, target):
            if i <= j:
                index = (i + j) // 2
                val = nums[index]
                if val == target:
                    return index
                elif val < target:
                    return binSearch(index + 1, j, nums, target)
                else:
                    return binSearch(i, index - 1, nums, target)
            return -1

        return binSearch(0, len(nums) - 1, nums, target)
