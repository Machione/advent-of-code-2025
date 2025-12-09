def add_quantum_numbers(diagram: str) -> list[list[int]]:
    diagram_lines = diagram.split()
    last_line = list(map(lambda x: 1 if x == "S" else 0, diagram_lines[0]))
    width = len(last_line)

    quants = []
    for line in diagram_lines[1:]:
        this_line = [0] * width
        for i, char in enumerate(list(line)):
            if char == ".":
                this_line[i] += last_line[i]

            if char == "^":
                if i > 0:
                    this_line[i - 1] += last_line[i]
                if i < width - 1:
                    this_line[i + 1] += last_line[i]

        last_line = this_line
        quants.append(this_line)

    return quants


def solve(diagram: str) -> int:
    quants = add_quantum_numbers(diagram)
    return sum(quants[-1])


if __name__ == "__main__":
    with open("day7/input.txt") as f:
        diagram = f.read()

    print(solve(diagram))
