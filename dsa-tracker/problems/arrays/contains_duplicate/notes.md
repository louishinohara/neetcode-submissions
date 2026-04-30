# Contains Duplicate

## Pattern
- hashing / set-membership

## Key Insight
- Trade space for time: a hash set turns the O(n^2) pairwise check into O(n).

## Mistake
- Reaching for sorting (O(n log n)) when a one-pass hash set is strictly better.

## Optimal Solution
- Iterate once; return True the moment a value repeats; otherwise add to the set.

## Time / Space Complexity
- Time: O(n)
- Space: O(n)

## Revisit
- Variant: Contains Duplicate II (k-distance) — use a sliding window of a hash set.
