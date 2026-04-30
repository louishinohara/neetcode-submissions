class Solution:
    def isValid(self, s: str) -> bool:
        vmap = {
            '}' : '{',
            ']' : '[',
            ')' : '('
        }

        stack = []

        for v in s:
            if v not in vmap:
                stack.append(v)
                continue
                
            if stack and stack[-1] == vmap[v]:
                stack.pop()
            else:
                return False
        
        return True if not stack else False
