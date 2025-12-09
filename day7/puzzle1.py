def solve(diagram: str) -> int:
    total_splits = 0
    diagram_lines = diagram.split()
    last_line = ["."] * len(diagram_lines[0])
    for line in diagram_lines:
        this_line = list(line)
        for i, char in enumerate(this_line):
            if char == ".":
                if last_line[i] == "S" or last_line[i] == "|":
                    this_line[i] = "|"
            elif char == "^" and last_line[i] == "|":
                total_splits += 1
                if i > 0 and this_line[i - 1] != "|":
                    this_line[i - 1] = "|"

                if i < len(this_line) - 2 and this_line[i + 2] != "^":
                    this_line[i + 1] = "|"

        last_line = this_line

    return total_splits


if __name__ == "__main__":
    with open("day7/input.txt") as f:
        diagram = f.read()

    print(solve(diagram))
