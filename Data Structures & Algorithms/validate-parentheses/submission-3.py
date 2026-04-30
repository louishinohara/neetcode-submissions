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
            else:
                if len(stack) == 0:
                    return False
                    
                i = stack[-1]
                if vmap[v] == i:
                    stack.pop()
                else:
                    return False
        
        if len(stack) == 0:
            return True

        return False