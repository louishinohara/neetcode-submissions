# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        
        def search(node, acc):
            # Base case
            if not node: return acc
            return max(search(node.left, acc + 1), search(node.right, acc + 1))

        return search(root, 0)