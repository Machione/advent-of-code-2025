import functools
import operator


def get_numbers(file_path: str) -> list[tuple[str, ...]]:
    lines = []
    with open(file_path) as f:
        for line in f:
            if len(line.strip().replace("+", "").replace("*", "").replace(" ", "")) > 0:
                lines.append(tuple(line.replace("\n", "")))

    return lines


def numbers_to_columns(numbers: list[tuple[str, ...]]) -> list[list[tuple[str, ...]]]:
    columns = []
    this_column: list[tuple[str, ...]] = []
    for x in range(len(numbers[0])):
        sub_column = tuple(line[x] for line in numbers)
        if all(c == " " for c in sub_column):
            columns.append(this_column)
            this_column = []
        else:
            this_column.append(sub_column)

    columns.append(this_column)
    return columns


def get_operations(file_path: str) -> tuple[str, ...]:
    with open(file_path) as file:
        for line in file:
            continue

    operations = tuple(s for s in line.strip().split())
    return operations


def collapse(column: list[tuple[str, ...]]) -> tuple[int, ...]:
    new_column = tuple(int("".join(v).replace(" ", "")) for v in column)
    return new_column


def solve(file_path: str) -> int:
    numbers = get_numbers(file_path)
    columns = numbers_to_columns(numbers)

    operations = get_operations(file_path)
    total = 0
    for i, operation in enumerate(operations):
        if operation == "+":
            op_func = operator.add

        if operation == "*":
            op_func = operator.mul

        this_column = collapse(columns[i])
        subtotal = functools.reduce(op_func, this_column)
        total += subtotal

    return total


if __name__ == "__main__":
    print(solve("day6/input.txt"))
