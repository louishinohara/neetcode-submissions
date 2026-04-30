# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        def helper(node):
            if not node: 
                return [True, 0]
            else:
                left, right = helper(node.left), helper(node.right)
                isBalanced = left[0] and right[0] and (abs(left[1] - right[1]) <= 1)
                return [isBalanced, 1 + max(left[1], right[1])]

        return helper(root)[0]
        
