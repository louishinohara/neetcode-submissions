# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        
        def helper(pNode, qNode):
            if not pNode and not qNode:       
                return True             

            if not pNode or not qNode:
                return False
        
            left = helper(pNode.left, qNode.left)
            right = helper(pNode.right, qNode.right)

            if pNode.val != qNode.val:
                return False

            return (left and right)

        return helper(p, q)


        