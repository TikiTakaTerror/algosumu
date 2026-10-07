import sys


class Grammar:
    def __init__(self, grammar_lines):
        self.name_to_id = {}
        self.id_to_name = []
        self.start = None

        raw_rules = []

        # Read the left sides first so the ids are fixed.
        # The rules are stored after that.
        for line in grammar_lines:
            parts = line.split("->", 1)
            left = parts[0].strip()
            right = parts[1].strip()

            if left not in self.name_to_id:
                new_id = len(self.id_to_name)
                self.name_to_id[left] = new_id
                self.id_to_name.append(left)

            # The assignment says the first left side is the start symbol.
            if self.start is None:
                self.start = self.name_to_id[left]

            raw_rules.append((left, right))

        self.num_nonterminals = len(self.id_to_name)

        # I keep the three linear rule types separate.
        self.terminal_rules = []
        self.left_terminal_rules = []
        self.right_terminal_rules = []

        for _ in range(self.num_nonterminals):
            self.terminal_rules.append(set())
            self.left_terminal_rules.append([])
            self.right_terminal_rules.append([])

        for rule in raw_rules:
            left = rule[0]
            right = rule[1]
            A = self.name_to_id[left]
            right_parts = right.split()

            if len(right_parts) == 1:
                terminal = right_parts[0]
                self.terminal_rules[A].add(terminal)

            elif len(right_parts) == 2:
                first = right_parts[0]
                second = right_parts[1]

                if first in self.name_to_id:
                    B = self.name_to_id[first]
                    terminal = second
                    self.right_terminal_rules[A].append((B, terminal))

                else:
                    terminal = first
                    B = self.name_to_id[second]
                    self.left_terminal_rules[A].append((terminal, B))


def read_input():
    # Standard input.
    lines = sys.stdin.read().splitlines()

    grammar_lines = []
    test_strings = []
    reading_grammar = True

    for line in lines:
        if reading_grammar:
            # The blank line separates the grammar from the test strings.
            if line.strip() == "":
                reading_grammar = False
            else:
                grammar_lines.append(line)
        else:
            # After the blank line, the remaining lines are test strings.
            test_strings.append(line)

    return grammar_lines, test_strings


class Parser:
    def __init__(self, grammar):
        self.grammar = grammar
        self.counter = 0

    def parseBU(self, text):
        self.counter = 0

        if len(text) == 0:
            return False

        n = len(text)
        number_of_symbols = self.grammar.num_nonterminals
        table = []

        # For bottom up I start the whole table as False.
        for _ in range(number_of_symbols):
            table_for_A = []

            for _ in range(n + 1):
                row = []

                for _ in range(n + 1):
                    row.append(False)

                table_for_A.append(row)

            table.append(table_for_A)

        # I first fill the table for parts with one character.
        for A in range(number_of_symbols):
            for i in range(n):
                character = text[i]

                if character in self.grammar.terminal_rules[A]:
                    table[A][i][i + 1] = True

        # Then I build the answers from shorter parts to longer parts.
        for length in range(2, n + 1):
            for i in range(0, n - length + 1):
                j = i + length

                for A in range(number_of_symbols):
                    found = False

                    # Try rules where the terminal is on the left.
                    for rule in self.grammar.left_terminal_rules[A]:
                        terminal = rule[0]
                        B = rule[1]
                        self.counter += 1

                        if text[i] == terminal and table[B][i + 1][j]:
                            table[A][i][j] = True
                            found = True
                            break

                    if found:
                        continue

                    # Try rules where the terminal is on the right.
                    for rule in self.grammar.right_terminal_rules[A]:
                        B = rule[0]
                        terminal = rule[1]
                        self.counter += 1

                        if table[B][i][j - 1] and text[j - 1] == terminal:
                            table[A][i][j] = True
                            break

        return table[self.grammar.start][0][n]


def main():
    grammar_lines, test_strings = read_input()

    if len(grammar_lines) == 0:
        return

    grammar = Grammar(grammar_lines)
    parser = Parser(grammar)

    for text in test_strings:
        result = parser.parseBU(text)

        if result:
            print("yes")
        else:
            print("no")


main()