"""
Regular Expression Matching
============================
Given an input string s and a pattern p, implement regular expression matching
with support for '.' and '*' where:
  - '.' matches any single character.
  - '*' matches zero or more of the preceding element.

The matching should cover the entire input string (not partial).

Approach: Bottom-Up Dynamic Programming
Time Complexity  : O(m × n)  where m = len(s), n = len(p)
Space Complexity : O(m × n)
"""


def is_match(s: str, p: str) -> bool:
    m, n = len(s), len(p)

    # dp[i][j] = True if s[:i] matches p[:j]
    dp = [[False] * (n + 1) for _ in range(m + 1)]

    # Base case: empty string matches empty pattern
    dp[0][0] = True

    # Handle patterns like a*, a*b*, a*b*c* that can match empty string
    for j in range(2, n + 1):
        if p[j - 1] == '*':
            dp[0][j] = dp[0][j - 2]

    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if p[j - 1] == '*':
                # Option 1: Use '*' as ZERO occurrences of preceding element
                # Eliminate the "x*" pair entirely
                zero_occurrence = dp[i][j - 2]

                # Option 2: Use '*' as ONE OR MORE occurrences
                # Current char of s must match the char before '*' in p
                preceding_char = p[j - 2]
                char_matches = (preceding_char == s[i - 1] or preceding_char == '.')
                one_or_more = dp[i - 1][j] if char_matches else False

                dp[i][j] = zero_occurrence or one_or_more

            elif p[j - 1] == '.' or p[j - 1] == s[i - 1]:
                # Current characters match (exact or wildcard '.')
                # Inherit result from the diagonal
                dp[i][j] = dp[i - 1][j - 1]

            else:
                # Characters don't match
                dp[i][j] = False

    return dp[m][n]


# ─────────────────────────────────────────────
#  Test Cases
# ─────────────────────────────────────────────

def run_tests():
    test_cases = [
        # (s, p, expected, description)
        ("aa",        "a",      False, "Pattern too short"),
        ("aa",        "a*",     True,  "Star repeats 'a' twice"),
        ("ab",        ".*",     True,  "'.*' matches any sequence"),
        ("aab",       "c*a*b",  True,  "c* = zero c's, a* = two a's"),
        ("mississippi","mis*is*p*.", False, "Classic tricky case"),
        ("",          "a*",     True,  "Zero occurrences match empty"),
        ("",          ".*",     True,  "Zero occurrences match empty"),
        ("a",         "ab*",    True,  "b* = zero b's"),
        ("aaa",       "a*a",    True,  "Greedy trap case"),
        ("aaa",       "ab*a",   False, "b* can't bridge gap"),
        ("",          "",       True,  "Both empty"),
        ("a",         ".",      True,  "Dot matches single char"),
        ("ab",        "a.",     True,  "Dot matches 'b'"),
    ]

    print("=" * 60)
    print(f"{'S':<15} {'P':<15} {'Expected':<10} {'Got':<10} {'Pass?'}")
    print("=" * 60)

    passed = 0
    for s, p, expected, desc in test_cases:
        result = is_match(s, p)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{repr(s):<15} {repr(p):<15} {str(expected):<10} {str(result):<10} {status}  {desc}")

    print("=" * 60)
    print(f"Results: {passed}/{len(test_cases)} passed\n")


if __name__ == "__main__":
    run_tests()

    # Interactive mode
    print("Try your own:")
    s = input("Enter string s: ").strip()
    p = input("Enter pattern p: ").strip()
    result = is_match(s, p)
    print(f"\nResult: {'✅ Match' if result else '❌ No Match'}")