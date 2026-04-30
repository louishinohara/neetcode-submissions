# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        
        # Switch the pointer of next to the current one
        # Then move to the next node and do the same

        prev = None # start
        curr = head #0

        # First iterate through the nodes until next is None which is how we know its over
        while curr is not None:
            nxt = curr.next # 0 points to 1
            curr.next = prev #0 now points to start
            prev = curr #prev is now 0
            curr = nxt #current is now 1

        return prev
