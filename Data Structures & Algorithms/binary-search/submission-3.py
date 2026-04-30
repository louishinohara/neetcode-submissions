class Solution:
    def search(self, nums: List[int], target: int) -> int:
        # Find the middle val
        # If its greater, then head is that index
        # If its less, tail is that index
        # When there is no more to search, return

        i, j = 0, len(nums) - 1

        # [0, 1] and target = 0
        # 1 - 0 = 1 / 2 = 0.5 -> ceiling = 1
        # what happens when there are two items? How to pick which one
        # floor -> 0 but what if it's 1?

        while i <= j:
            index = math.floor((j+i)/2)
            val = nums[index]
            if val == target:
                return index
            elif val < target:
                i = index + 1
            else:
                j = index - 1

        return -1
