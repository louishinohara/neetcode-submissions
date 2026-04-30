class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        # 1st sol
        # Create a map then get the max vals

        h = {}
        for num in nums:
            if num not in h:
                h[num] = 1
            else:
                h[num] += 1
        
        # iterate through map to get the vals
        arr = [k for k, v in sorted(h.items(), key=lambda x: x[1], reverse=True)]
        return arr[:k]
        