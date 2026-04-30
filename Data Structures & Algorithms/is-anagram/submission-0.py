class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # sort and compare list NLOG(N)
        # hash and compare O(n)

        if len(s) != len(t):
            return False

        sSorted = sorted(s)
        tSorted = sorted(t)

        for i, n in enumerate(sSorted):
            if tSorted[i] != n:
                return False
        
        return True
        
        