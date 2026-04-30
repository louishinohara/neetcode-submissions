class Solution:
    def isValid(self, s: str) -> bool:
        vmap = {
            '}' : '{',
            ']' : '[',
            ')' : '('
        }

        stack = []

        for v in s:
            if v in vmap:
                if stack and stack[-1] == vmap[v]:
                    stack.pop()
                else:
                    return False
            else:
                stack.append(v)
        
        return True if not stack else False
