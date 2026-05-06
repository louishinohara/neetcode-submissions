class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 2: return n
        res = [0, 1, 2]

        for i in range(3, n+1):
            print(i, res, res[i-1] + res[i-2])
            res.append(res[i-1] + res[i-2])
        return res[-1]
