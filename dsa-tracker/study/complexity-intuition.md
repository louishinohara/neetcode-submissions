# Complexity intuition — focus areas to harden

_Captured 2026-05-02 from binary search practice (iterative + recursive)._

## 1. log n intuition (binary search core)
- Repeatedly halving input → `n → n/2 → n/4 → ...`
- "How many times can I divide by 2 until 1?" → that count = `log n`.

## 2. Time vs space are separate
- **Time** = how many total operations.
- **Space** = max memory used at one moment.
- One does not imply the other.

## 3. Why recursion = O(log n) space (binary search case)
- Each call adds a stack frame.
- Depth of calls = `log n`.
- Stack depth = space usage.

## 4. Why iteration = O(1) space
- No call stack growth.
- Only fixed variables (`l`, `r`, `mid`).
- Memory does not scale with input size.

## 5. When recursion becomes worse than log n space
Depth depends on the structure of the recursion tree:
- Binary split → `log n`
- Chain (linked list, skewed tree) → `n`

Key question: **how deep does recursion go?**

## 6. n log n concept
Happens when:
- Recursion depth = `log n`
- Work per level = `n`

Example pattern: divide + combine work each level (merge sort).
Key idea: **log levels × work per level**.

## 7. Core mental-model shift
- Not "½ × ½ × ½ = log n".
- Instead:
  - **Count of halvings → `log n`**
  - **Structure of recursion tree → determines time/space**

---

## Open todo
- [ ] Build a quick "pattern map": when problems become `O(n)`, `O(log n)`, `O(n log n)`, `O(n²)` instantly. Trigger this when picking up a new problem and asking "what shape is the work tree?"
