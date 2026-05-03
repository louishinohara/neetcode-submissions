# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        
        def compare(a, b):
            if a is None and b is None:
                return True
            
            if a is None and b:
                return False
            if a and b is None:
                return False

            if a.val == b.val:
                leftRes = False
                if a.left and b.left:
                    leftRes = compare(a.left, b.left)
                else:
                    if a.left is None and b.left is None:
                        leftRes = True

                rightRes = False
                if a.right and b.right:
                    rightRes = compare(a.right, b.right)
                else:
                    if a.right is None and b.right is None:
                        rightRes = True

                return leftRes and rightRes

            return False

        
        return compare(p, q)

