import numpy
import pandas


def get_numbers(file_path: str) -> pandas.DataFrame:
    df = pandas.read_table(file_path, sep=r"\s+", header=None, skipfooter=1)
    return df


def get_operations(file_path: str) -> tuple[str, ...]:
    with open(file_path) as file:
        for line in file:
            continue

    operations = tuple(s for s in line.strip().split())
    return operations


def solve_columns(file_path: str) -> list[numpy.int64]:
    numbers = get_numbers(file_path)
    operations = get_operations(file_path)

    solutions = []
    for i, column in enumerate(numbers.columns):
        this_column = numbers[column]
        this_operation = operations[i]

        if this_operation == "*":
            this_solution = this_column.product()
            if isinstance(this_solution, numpy.int64):
                solutions.append(this_solution)
        elif this_operation == "+":
            this_solution = this_column.sum()
            if isinstance(this_solution, numpy.int64):
                solutions.append(this_solution)

    return solutions


def solve(file_path: str) -> int:
    columns = solve_columns(file_path)
    soln = numpy.array(columns).sum()
    return int(soln)


if __name__ == "__main__":
    print(solve("day6/input.txt"))
