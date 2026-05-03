# Binary Search

## Pattern
- binary search (sorted array, target lookup)

## Key Insight
- Maintain the `lo <= hi` invariant; on each step, drop the half that cannot contain the target.
- Recursive and iterative are equivalent algorithmically. In Python prefer iterative — no tail-call optimization, and recursion costs an extra O(log n) stack frames.

## Mistake
- Recursive draft compared `mid < target` instead of `nums[mid] < target` — comparing the index to the value instead of the value at the index. Read what you wrote out loud.
- Shrinking must be `mid + 1` / `mid - 1`, never just `mid`, or the search loops forever when the target is absent.

## Optimal Solution
- Iterative two-pointer with `mid = (lo + hi) // 2`. Returns `-1` when `lo > hi`.

## Time / Space Complexity
- Time: O(log n)
- Space: O(1) iterative, O(log n) recursive (call stack)

## Revisit
- Variants: search insert position, first/last occurrence of target, search a 2D matrix, koko eating bananas (binary-search on the answer space).
- Concept review: see `study/complexity-intuition.md` (log n intuition, time vs space, recursion depth → space, n log n shape).
