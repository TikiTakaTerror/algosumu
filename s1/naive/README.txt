Step 1 - Naive

This is my implementation of the naive recursive CYK parser.

When reading the grammar I give each nonterminal an integer id. I store terminal rules and binary rules separately so they can be accessed directly when parsing.

This version follows the recursive algorithm without memoization. The counter is reset for every test string and is increased for every call to the recursive parser.

The program is run using run.sh. It reads the grammar and test strings from standard input and prints yes or no for each test string.

For testing I mainly used the balanced parentheses grammar from the assignment and also some smaller CNF grammars.

Limitations:
The naive version gets very slow for longer strings since it calculates the same subproblems many times. This is expected for this version.

Empty strings are not handled. I kept the implementation to the algorithm described in Step 1, which starts with the case of a single character.
