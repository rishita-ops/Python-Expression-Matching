# Python — Expression Matching

A focused Python implementation that **decides whether an entire input string matches a pattern containing `.` and `*`** using a **bottom-up dynamic programming table**. Clean, compact, and correct — this program is the entry point to understanding 2D DP on two strings, how `*` creates a branching decision (zero occurrences vs. one or more), and why a table of `(m + 1) × (n + 1)` booleans turns an exponential recursion into an O(m × n) solution. Pattern matching is also a small, honest look at how regular-expression engines think.

🔗 **Related LeetCode problem:** [Regular Expression Matching](https://leetcode.com/problems/regular-expression-matching/) (#10, Hard)

---

## Problem Statement

Given an input string `s` and a pattern `p`, implement regular expression matching with support for two special characters:

| Symbol | Meaning                                           |
| ------ | ------------------------------------------------- |
| `.`    | Matches **any single character**                  |
| `*`    | Matches **zero or more** of the preceding element |

The match must cover the **entire** input string, not just a part of it. Return `True` if `s` matches `p`, otherwise `False`.

**Example Input:**

```
Enter the string s: aab
Enter the pattern p: c*a*b
```

**Example Output:**

```
True
```

**More examples:**

```
s = "aa",  p = "a"      → False   (pattern is too short)
s = "aa",  p = "a*"     → True    (a* = two a's)
s = "ab",  p = ".*"     → True    (.* = any sequence)
s = "aab", p = "c*a*b"  → True    (c* = zero c's, a* = two a's, then b)
```

**How this differs from the official LeetCode wording:** LeetCode calls a method on a `Solution` class (`isMatch`) and guarantees a valid pattern, where every `*` has a valid character before it. This version is a standalone function with a small input driver, and it relies on the same guarantee.

---

## The Code

```python
# Regular Expression Matching — bottom-up dynamic programming
# '.' matches any single character, '*' matches zero or more of the preceding element
# ex : s = "aab", p = "c*a*b"  ->  True
def is_match(s, p):
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[0][0] = True                      # empty string matches empty pattern

    # empty string vs. patterns like "a*b*c*": each "x*" pair can vanish
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                dp[i][j] = dp[i][j - 2]                          # zero occurrences
                if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                    dp[i][j] = dp[i][j] or dp[i - 1][j]          # one or more occurrences
            elif p[j - 1] == s[i - 1] or p[j - 1] == '.':
                dp[i][j] = dp[i - 1][j - 1]                      # plain character match
    return dp[m][n]
```

---

## The Critical Idea — A Table of Prefix Matches

This is the most important thing to understand about this program.

**Define one question for every pair of prefixes:**

```
dp[i][j] = True  if  s[:i]  matches  p[:j]
```

The table has `m + 1` rows (prefixes of `s`, including the empty one) and `n + 1` columns (prefixes of `p`, including the empty one). Every cell is answered **once**, using only cells that are already filled in. The answer to the whole problem is the bottom-right cell, `dp[m][n]`.

### Base cases

```
dp[0][0] = True            # empty string matches empty pattern
dp[0][j] = dp[0][j-2]      # when p[j-1] == '*', the pair "x*" can match nothing
```

### Transitions

```
Case 1 — p[j-1] is NOT '*':
    dp[i][j] = dp[i-1][j-1]     if p[j-1] == s[i-1]  or  p[j-1] == '.'
               (otherwise False)

Case 2 — p[j-1] IS '*':
    Option A (zero occurrences):  dp[i][j-2]
    Option B (one or more):       dp[i-1][j]    if p[j-2] == s[i-1]  or  p[j-2] == '.'
    dp[i][j] = Option A  or  Option B
```

| Approach                     | Time         | Extra space    | Notes                                          |
| ---------------------------- | ------------ | -------------- | ---------------------------------------------- |
| Plain recursion              | Exponential  | O(m + n) stack | Re-solves the same subproblems again and again |
| Top-down recursion + memo    | O(m × n)     | O(m × n)       | Same idea as the table, written recursively    |
| **Bottom-up DP (this code)** | **O(m × n)** | O(m × n)       | Simple loops, no recursion limit               |
| Bottom-up DP + rolling row   | O(m × n)     | **O(n)**       | Row `i` only needs row `i − 1`                 |

Plain recursion is the right _first_ idea to write, because it is easy to prove correct. The table is that same recursion with the repeated work removed.

---

## How the Loops Work

```python
for i in range(1, m + 1):
    for j in range(1, n + 1):
        if p[j - 1] == '*':
            ...
        elif p[j - 1] == s[i - 1] or p[j - 1] == '.':
            ...
```

- **Outer loop:** `i` runs `1 … m` — how many characters of `s` are in the prefix
- **Inner loop:** `j` runs `1 … n` — how many characters of `p` are in the prefix
- **`*` branch:** combines _zero occurrences_ (`dp[i][j-2]`) with _one or more occurrences_ (`dp[i-1][j]`)
- **Plain branch:** a letter or `.` must match the current character, and the previous prefixes must already match (`dp[i-1][j-1]`)
- **Result:** after both loops finish, `dp[m][n]` holds the answer

> **Index note:** the table is shifted by one. `dp[i][j]` describes the _first `i`_ characters of `s`, so the character being examined is `s[i - 1]`, not `s[i]`. The same applies to `p[j - 1]`. Mixing these up is the most common bug in this problem.

---

## The Greedy Trap

Consider `s = "aaa"` and `p = "a*a"`.

A greedy matcher lets `a*` consume **all three** `a`'s, and then fails because the final `a` in the pattern has nothing left to match. The correct answer is `True`: `a*` takes two `a`'s and the last `a` takes the third.

The DP table never commits to one choice. For every `*`, it keeps **both** the zero-occurrence path and the one-or-more path alive at the same time:

| `s` prefix \ `p` prefix | `""` | `a` | `a*` | `a*a`    |
| ----------------------- | ---- | --- | ---- | -------- |
| `""`                    | T    | F   | T    | F        |
| `a`                     | F    | T   | T    | T        |
| `aa`                    | F    | F   | T    | T        |
| `aaa`                   | F    | F   | T    | **T** ✅ |

---

## Algorithm (Pseudocode)

```
read s and p
m <- length of s
n <- length of p

create table dp of size (m+1) x (n+1), all False
dp[0][0] <- True

for j from 2 to n:
    if p[j-1] is '*':
        dp[0][j] <- dp[0][j-2]

for i from 1 to m:
    for j from 1 to n:
        if p[j-1] is '*':
            dp[i][j] <- dp[i][j-2]
            if p[j-2] equals s[i-1] or p[j-2] is '.':
                dp[i][j] <- dp[i][j] or dp[i-1][j]
        else if p[j-1] equals s[i-1] or p[j-1] is '.':
            dp[i][j] <- dp[i-1][j-1]

report dp[m][n]
```

---

## Dry Run

**Input:** `s = "aab"`, `p = "c*a*b"`

Columns are prefixes of `p`; rows are prefixes of `s`.

|           | `""` | `c` | `c*` | `c*a` | `c*a*` | `c*a*b`  |
| --------- | ---- | --- | ---- | ----- | ------ | -------- |
| **`""`**  | T    | F   | T    | F     | T      | F        |
| **`a`**   | F    | F   | F    | T     | T      | F        |
| **`aa`**  | F    | F   | F    | F     | T      | F        |
| **`aab`** | F    | F   | F    | F     | F      | **T** ✅ |

**How a few cells are decided:**

| Cell                        | Rule used                                   | Value |
| --------------------------- | ------------------------------------------- | ----- |
| `dp[0][2]` (`""`, `c*`)     | `*` can drop the pair `c*` → `dp[0][0]`     | T     |
| `dp[1][3]` (`a`, `c*a`)     | `a` matches `a`, and `dp[0][2]` is T        | T     |
| `dp[1][4]` (`a`, `c*a*`)    | one occurrence of `a*` → `dp[0][4]` is T    | T     |
| `dp[2][4]` (`aa`, `c*a*`)   | `a*` absorbs a second `a` → `dp[1][4]` is T | T     |
| `dp[3][5]` (`aab`, `c*a*b`) | `b` matches `b`, and `dp[2][4]` is T        | T     |

**Output:** `True` ✅

---

## Complexity Analysis

| Metric            | Complexity                                                                               |
| ----------------- | ---------------------------------------------------------------------------------------- |
| Time (all cases)  | **O(m × n)** — every cell of the `(m+1) × (n+1)` table is computed exactly once, in O(1) |
| Space             | **O(m × n)** — the full table is stored                                                  |
| Space (optimized) | **O(n)** — a rolling row works because row `i` only reads row `i` and row `i − 1`        |

Where `m = len(s)` and `n = len(p)`.

---

## Edge Cases

| Scenario                                   | Behavior                                                                |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| `s = ""`, `p = "a*"`                       | `a*` matches zero `a`'s — returns `True` ✅                             |
| `s = ""`, `p = "a*b*c*"`                   | Every `x*` pair vanishes — returns `True` ✅                            |
| `s = ""`, `p = "a"`                        | A plain letter cannot match nothing — returns `False` ✅                |
| `s = "a"`, `p = ""`                        | Nothing left in the pattern to match the character — returns `False` ✅ |
| `s = "ab"`, `p = ".*"`                     | `.*` matches any sequence — returns `True` ✅                           |
| `s = "ab"`, `p = ".*c"`                    | The final `c` has nothing to match — returns `False` ✅                 |
| `s = "aaa"`, `p = "a*a"`                   | Greedy trap — `a*` must give one `a` back — returns `True` ✅           |
| `s = "a"`, `p = "ab*"`                     | `b*` matches zero `b`'s — returns `True` ✅                             |
| `s = "mississippi"`, `p = "mis*is*p*."`    | Looks close, but characters are left over — returns `False` ✅          |
| Pattern starting with `*` (such as `"*a"`) | Invalid input — `p[j - 2]` would wrap to the last character ⚠️          |
| Two stars in a row (such as `"a**"`)       | Invalid input — not covered by the problem's guarantee ⚠️               |

---

## Code-Quality Notes

**The function assumes a valid pattern.** LeetCode guarantees that every `*` follows a valid character. If a pattern starts with `*`, the expression `p[j - 2]` becomes `p[-1]` (the _last_ character) and the result is silently wrong. A reusable version should validate the pattern first, or raise `ValueError`.

**The function returns a boolean, not a message.** This is the right design: the caller decides how to print the result, and it is easy to test.

**Not a direct LeetCode submission.** LeetCode calls a method on a class, so the standalone function above will not run in the LeetCode editor as it is. The submittable version is:

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[0][0] = True
        for j in range(2, n + 1):
            if p[j - 1] == '*':
                dp[0][j] = dp[0][j - 2]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if p[j - 1] == '*':
                    dp[i][j] = dp[i][j - 2]
                    if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                        dp[i][j] = dp[i][j] or dp[i - 1][j]
                elif p[j - 1] == s[i - 1] or p[j - 1] == '.':
                    dp[i][j] = dp[i - 1][j - 1]
        return dp[m][n]
```

**The file defines the function but never calls it.** Running only `is_match` prints nothing. The "How to Compile and Run" section below includes a small driver that adds the input part.

---

## The Natural Extension — Rolling Row (O(n) Space)

Row `i` of the table only depends on row `i − 1` and on cells to its own left, so the full table is not needed. Two rows are enough:

```python
def is_match_rolling(s, p):
    m, n = len(s), len(p)
    prev = [False] * (n + 1)
    prev[0] = True
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            prev[j] = prev[j - 2]

    for i in range(1, m + 1):
        cur = [False] * (n + 1)
        for j in range(1, n + 1):
            if p[j - 1] == '*':
                cur[j] = cur[j - 2]
                if p[j - 2] == s[i - 1] or p[j - 2] == '.':
                    cur[j] = cur[j] or prev[j]
            elif p[j - 1] == s[i - 1] or p[j - 1] == '.':
                cur[j] = prev[j - 1]
        prev = cur
    return prev[n]
```

**Result:** the same answers as the full table, using `O(n)` extra space instead of `O(m × n)`.

| Property       | Full table (this code)        | Rolling row                         |
| -------------- | ----------------------------- | ----------------------------------- |
| Time           | O(m × n)                      | O(m × n)                            |
| Extra space    | O(m × n)                      | **O(n)**                            |
| Easy to debug? | ✅ Whole table can be printed | Only the current row is visible     |
| When to use    | Learning, small inputs        | Long strings, memory-sensitive code |

---

## Test Cases

| `s`             | `p`            | Expected | Note                |
| --------------- | -------------- | -------- | ------------------- |
| `"aa"`          | `"a"`          | `False`  | Pattern too short   |
| `"aa"`          | `"a*"`         | `True`   | Star repeats        |
| `"ab"`          | `".*"`         | `True`   | Wildcard sequence   |
| `"aab"`         | `"c*a*b"`      | `True`   | Zero c's, two a's   |
| `"mississippi"` | `"mis*is*p*."` | `False`  | Classic tricky case |
| `""`            | `"a*"`         | `True`   | Zero occurrences    |
| `"aaa"`         | `"a*a"`        | `True`   | Greedy trap         |

---

## Repository Structure

```
Python-Expression-Matching/
│
├── solution.py     # Main Python implementation
└── README.md       # Project documentation
```

---

## How to Compile and Run

**Prerequisites:** Python 3.8+

Add this driver below the function in `solution.py` so the program reads input as described in the comments:

```python
s = input("Enter the string s: ")
p = input("Enter the pattern p: ")
print(is_match(s, p))
```

```bash
# Clone the repository
git clone https://github.com/<your-username>/Python-Expression-Matching.git
cd Python-Expression-Matching

# Run
python3 solution.py
```

**On Windows:**

```bash
python solution.py
```

**Sample session:**

```
Enter the string s: aab
Enter the pattern p: c*a*b
True
```

---

## Key Concepts Covered

- **2D dynamic programming** — one cell per pair of prefixes `(s[:i], p[:j])`
- **Overlapping subproblems** — the table removes the repeated work of plain recursion
- **The `*` decision** — zero occurrences (`dp[i][j-2]`) versus one or more (`dp[i-1][j]`)
- **Greedy fails** — `a*` cannot blindly consume every `a`, as `"aaa"` vs `"a*a"` shows
- **Base cases that matter** — `"a*b*c*"` must be able to match the empty string
- **One-based table over zero-based strings** — `dp[i][j]` uses `s[i - 1]` and `p[j - 1]`
- **Rolling arrays** — reducing space from O(m × n) to O(n)
- **`.*` is not the same as a bare `*`** — a `*` always needs a preceding element

---

## Why This Problem Matters in DSA

Matching one sequence against another with a table of prefixes appears across a broad family of problems:

| Problem / Concept                               | Connection                                                            |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| **Regular Expression Matching** (LeetCode #10)  | The problem this solution is based on                                 |
| **Wildcard Matching** (LeetCode #44)            | Same table; `?` is `.`, and `*` matches any sequence by itself        |
| **Edit Distance** (LeetCode #72)                | Same two-string prefix table, counting operations instead of booleans |
| **Interleaving String** (LeetCode #97)          | Boolean table over prefixes of two strings                            |
| **Distinct Subsequences** (LeetCode #115)       | Prefix table that counts how many ways one string forms another       |
| **Longest Common Subsequence** (LeetCode #1143) | The classic template for `dp[i][j]` over two strings                  |

**Connection to automata theory:** a pattern like this describes a **finite automaton**, and the DP table tracks which automaton states are reachable after reading each prefix of `s`. Engines such as RE2 and `grep` work this way. Python's built-in `re` module takes a different route (backtracking), which is why some patterns can be catastrophically slow there but never here.

---

## Contributing

Contributions are welcome. Consider adding:

- A **test runner** that checks the table of test cases above and prints a pass/fail summary
- An **interactive mode** that keeps asking for new `s` and `p` pairs
- The **rolling-row** version as a separate file for side-by-side comparison
- A **top-down memoized** version using `functools.lru_cache`
- **Input validation** for patterns that start with `*` or contain `**`
- Implementations in C++, Java, or JavaScript

```bash
git checkout -b feature/your-feature
git commit -m "Add: your feature description"
git push origin feature/your-feature
# Then open a Pull Request
```

---

## License

This project is open-source and available under the [MIT License](LICENSE).

---

_Part of a structured LeetCode practice series — fundamentals, done right._
