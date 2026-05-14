class Solution:
    def isValid(self, s: str) -> bool:
        stack = []        
        k = {
            ')':'(',
            '}':'{',
            ']':'['
        }

        
        for item in s:
            if stack and item in k:
                last = stack.pop()
                if last != k[item]:
                    return False
            else:
                stack.append(item)
        
        return False if stack else True