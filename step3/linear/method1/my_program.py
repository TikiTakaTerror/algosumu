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

        # Terminals in two symbol rules need a new nonterminal.
        terminal_names = {}

        for rule in raw_rules:
            right = rule[1]
            right_parts = right.split()

            if len(right_parts) == 2:
                for symbol in right_parts:
                    if symbol not in self.name_to_id:
                        if symbol not in terminal_names:
                            new_name = "_T" + str(len(terminal_names))

                            while new_name in self.name_to_id:
                                new_name = "_" + new_name

                            new_id = len(self.id_to_name)
                            self.name_to_id[new_name] = new_id
                            self.id_to_name.append(new_name)

                            terminal_names[symbol] = new_name

        self.num_nonterminals = len(self.id_to_name)

        # I keep the two CNF rule types separate.
        self.terminal_rules = []
        self.binary_rules = []

        for _ in range(self.num_nonterminals):
            self.terminal_rules.append(set())
            self.binary_rules.append([])

        # Convert the linear rules to ordinary CNF rules.
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

                if first in terminal_names:
                    first = terminal_names[first]

                if second in terminal_names:
                    second = terminal_names[second]

                B = self.name_to_id[first]
                C = self.name_to_id[second]
                self.binary_rules[A].append((B, C))

        # Add the terminal rules for the new nonterminals.
        for terminal, name in terminal_names.items():
            A = self.name_to_id[name]
            self.terminal_rules[A].add(terminal)


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

                    # For a longer part, try the binary rules for A.
                    for rule in self.grammar.binary_rules[A]:
                        B = rule[0]
                        C = rule[1]

                        # Try the places where the string can be split.
                        for k in range(i + 1, j):
                            self.counter += 1

                            if table[B][i][k] and table[C][k][j]:
                                table[A][i][j] = True
                                found = True
                                break

                        if found:
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