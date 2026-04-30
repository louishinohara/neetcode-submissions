# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def diameterOfBinaryTree(self, root: Optional[TreeNode]) -> int:
        
        def helper(node):
            if not node: return [0, 0]

            # Traverse to leaf
            left = helper(node.left)
            right = helper(node.right)
            
            # Add edge counter if node exists
            if node.left: left[0] += 1
            if node.right: right[0] += 1
            
            # Return current max depth to keep track of DFS, Return longest path based on existing max depth
            return [max(left[0], right[0]), max(left[0] + right[0], left[1], right[1])]
        
        return helper(root)[1]




