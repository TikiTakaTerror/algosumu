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
        self.text = ""
        self.counter = 0

    def parseNaive(self, text):
        self.text = text
        self.counter = 0

        if len(text) == 0:
            return False

        return self.parsePart(self.grammar.start, 0, len(text))

    def parsePart(self, A, i, j):
        # A is the nonterminal I am checking and i,j are the part
        # of the string I am checking.
        self.counter += 1

        # If there is only one character, check the terminal rule.
        if j == i + 1:
            character = self.text[i]
            if character in self.grammar.terminal_rules[A]:
                return True
            return False

        # For a longer part, try the binary rules for A.
        for rule in self.grammar.binary_rules[A]:
            B = rule[0]
            C = rule[1]

            # Try the possible places where the string can be split.
            for k in range(i + 1, j):
                # Check if B can make the left part first.
                left_result = self.parsePart(B, i, k)

                if left_result:
                    # If that worked, check C on the right part.
                    right_result = self.parsePart(C, k, j)
                    if right_result:
                        return True

        # Nothing worked for this part of the string.
        return False


def main():
    grammar_lines, test_strings = read_input()

    if len(grammar_lines) == 0:
        return

    grammar = Grammar(grammar_lines)
    parser = Parser(grammar)

    for text in test_strings:
        result = parser.parseNaive(text)

        if result:
            print("yes")
        else:
            print("no")


main()
