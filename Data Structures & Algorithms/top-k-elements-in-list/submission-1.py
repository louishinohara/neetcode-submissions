class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:        
        # First create a map to store the values
        hmap = {}
        # Second create buckets to store actual values using length of list as number of buckets
        arr = [[] for i in range(len(nums)+1)]
        # Third, populate map with values
        
        for num in nums: hmap[num] = hmap.get(num, 0) + 1

        # Using map, append numbers to index which is the frequency of appearance
        for x, v in hmap.items():
            arr[v].append(x)
        
        sol = []
        index = len(arr) - 1
        # Starting from the end, grab numbers of appearances
        while k > 0:
            a = arr[index]
            for number in a:
                sol.append(number)
                k -= 1
            index -= 1
        return sol



