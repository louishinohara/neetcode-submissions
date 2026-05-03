# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        
        def traverse(p, counter):
            if not p: return counter
            
            return max(traverse(p.left, counter + 1), (traverse(p.right, counter + 1)))
        
        return traverse(root, 0)