Step 1  Bottom-up

This is my implementation of the bottom up CYK parser.

When reading the grammar, nonterminals are given integer ids. Terminal and binary rules are stored separately.

For this version I use a table. I first fill the entries for parts with one character. After that I work from shorter parts to longer parts so the smaller results are already available when I need them.

The counter is reset for every test string and is increased in the innermost split point loop.

The program reads the grammar and test strings from standard input and prints yes or no for each test string.

I mainly tested it using the balanced parentheses grammar from the assignment and some smaller CNF grammars.

Limitations:
No known limitations for the required Step 1 functionality.
