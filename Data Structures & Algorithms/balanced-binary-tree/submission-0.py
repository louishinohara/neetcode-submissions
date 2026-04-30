# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:
        # Check node height at each level
        # Need to keep an accum for both sides
        # Need a way to "self exit"
            # Need to pass boolean. Boolean is for comparison

        # How can we return bool and a value?
        # Issue with the accum
        def helper(node):
            
            # Base case, empty returns True
            if not node: return [True, 0]

            # Need an acc to keep track of the height on both sides
                # max depth of either side. And compare on that node

            # Need to post order
            # collect val on the way back up
            left = helper(node.left)
            right = helper(node.right)

            balanced = left[0] and right[0] and (abs(left[1] - right[1]) <= 1)

            return [balanced, 1 + max(left[1], right[1])]

        return helper(root)[0]
        
