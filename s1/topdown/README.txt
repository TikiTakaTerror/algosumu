Step 1  Top-down

This is my implementation of the top down CYK parser with memoization.

When reading the grammar, nonterminals are given integer ids. Terminal and binary rules are stored separately.

The main difference from the naive version is the memoization table. I use None for a result that has not been calculated yet. After a result is found, True or False is saved so the same subproblem does not need to be calculated again.

The counter is reset for every test string and counts calls to the recursive parser.

The program reads the grammar and test strings from standard input and prints yes or no for each test string.

I mainly tested it using the balanced parentheses grammar from the assignment and some smaller CNF grammars.

Limitations:
No known limitations for the required Step 1 functionality.
