class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2: return n

        def helper(a, b, c):
            if c == 0:
                return b
            return helper(b, a+b, c-1)

        return helper(1,2,n-2)