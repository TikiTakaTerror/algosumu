This implementation is based on the bottom-up parser from Step 1.

It has been changed to work directly with linear grammar rules of the forms A -> a, A -> aB, and A -> Ba. Since one side of a linear rule is always a terminal, the parser does not need to try all split positions as in ordinary CYK.

The program reads the grammar and test strings from standard input and prints yes or no for each test string.