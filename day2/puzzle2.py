from collections.abc import Collection


def get_start_point_from_range(r: str) -> int:
    return int(r[: r.index("-")])


def get_end_point_from_range(r: str) -> int:
    return int(r[r.index("-") + 1 :])


def get_all_values_in_range(r: str) -> tuple[str, ...]:
    start_point = get_start_point_from_range(r)
    end_point = get_end_point_from_range(r)

    values = tuple(str(num) for num in range(start_point, end_point + 1))
    return values


def is_value_valid(v: str) -> bool:
    if len(v) == 0:
        return True

    for dup_length in range(1, (len(v) // 2) + 1):
        if len(v) % dup_length != 0:
            continue

        chars_to_check = v[:dup_length]
        repeats = len(v) // dup_length
        if v == chars_to_check * repeats:
            return False

    return True


def find_invalid_values_in_range(r: str) -> list[int]:
    invalid_values = []
    values = get_all_values_in_range(r)
    for v in values:
        if is_value_valid(v) is False:
            invalid_values.append(int(v))

    return invalid_values


def sum_invalid_values(ranges: Collection[str]) -> int:
    invalid_values = []
    for r in ranges:
        invalid_values += find_invalid_values_in_range(r)

    return sum(invalid_values)


if __name__ == "__main__":
    total = 0
    with open("day2/input.txt") as file:
        for line in file:
            ranges = line.split(",")
            total += sum_invalid_values(ranges)

    print(total)
