import sys
import time


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

        # Some nonterminals may only appear on the right side,
        # so add those too.
        for rule in raw_rules:
            right = rule[1]
            right_parts = right.split()

            if len(right_parts) == 2:
                for name in right_parts:
                    if name not in self.name_to_id:
                        new_id = len(self.id_to_name)
                        self.name_to_id[name] = new_id
                        self.id_to_name.append(name)

        self.num_nonterminals = len(self.id_to_name)

        # I keep the two CNF rule types separate.
        self.terminal_rules = []
        self.binary_rules = []

        for _ in range(self.num_nonterminals):
            self.terminal_rules.append(set())
            self.binary_rules.append([])

        # Convert the rule names to ids here instead of doing it
        # while parsing.
        for rule in raw_rules:
            left = rule[0]
            right = rule[1]
            A = self.name_to_id[left]
            right_parts = right.split()

            if len(right_parts) == 1:
                terminal = right_parts[0]
                self.terminal_rules[A].add(terminal)

            elif len(right_parts) == 2:
                B = self.name_to_id[right_parts[0]]
                C = self.name_to_id[right_parts[1]]
                self.binary_rules[A].append((B, C))


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

    # Warm up once with the longest test string.
    if len(test_strings) > 0:
        longest = max(test_strings, key=len)
        parser.parseBU(longest)

    for text in test_strings:
        times = []
        result = False
        operations = 0

        # Run the same test ten times.
        for _ in range(10):
            start_time = time.perf_counter()
            result = parser.parseBU(text)
            end_time = time.perf_counter()

            times.append(end_time - start_time)
            operations = parser.counter

        # Remove the fastest and slowest time.
        times.sort()
        used_times = times[1:-1]
        average_time = sum(used_times) / len(used_times)

        answer = "yes" if result else "no"
        print("bottomup," + str(len(text)) + "," + answer + ","
              + str(operations) + "," + str(average_time))


main()
