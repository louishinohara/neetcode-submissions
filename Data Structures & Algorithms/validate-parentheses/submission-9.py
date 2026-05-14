class Solution:
    def isValid(self, s: str) -> bool:
        if len(s) == 0: return True
        elif len(s) == 1: return False

        k = {
            '(':')',
            '{':'}',
            '[':']'
        }

        stack = []
        for item in s:
            if item in k.keys():
                stack.append(item)
            else:
                if len(stack) == 0: return False
                last = stack.pop()
                if k[last] == item:
                    continue
                else:
                    return False
        
        return len(stack) == 0