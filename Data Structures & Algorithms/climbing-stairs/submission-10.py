class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2: return n
        i, j = 1, 2

        for z in range(3, n+1):
            k = i + j
            i, j = j, k
        return k
