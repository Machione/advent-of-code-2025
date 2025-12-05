def find_ranges(s: str) -> list[str]:
    ranges: list[str] = []
    for line in s.split():
        clean_line = line.strip()
        if "-" not in clean_line:
            return ranges

        if len(clean_line) > 0:
            ranges.append(clean_line)

    return ranges


def find_fresh_ingredient_ids(ranges: list[str]) -> list[tuple[int, int]]:
    fresh_id_ragnes: list[tuple[int, int]] = []
    for r in ranges:
        start_id, end_id = r.split("-")
        this_range = (int(start_id), int(end_id))
        fresh_id_ragnes.append(this_range)

    return fresh_id_ragnes


def simplify_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    found_ranges: list[tuple[int, int]] = []
    for this_start, this_end in ranges:
        extends = False
        for found_start, found_end in found_ranges:
            if (
                (
                    this_start <= found_start and this_end >= found_end
                )  # This totally encloses found
                or (
                    this_start >= found_start and this_start <= found_end
                )  # This extends found on the right
                or (
                    this_end >= found_start and this_end <= found_end
                )  # This extends found on the left
            ):
                extends = True
                found_ranges.remove((found_start, found_end))
                new_start = min(this_start, found_start)
                new_end = max(this_end, found_end)
                found_ranges.append((new_start, new_end))

        if extends is False:
            found_ranges.append((this_start, this_end))

    return found_ranges


def de_overlap_ranges(ranges: list[tuple[int, int]]) -> list[tuple[int, int]]:
    last_size = len(ranges)
    ranges = simplify_ranges(ranges)
    this_size = len(ranges)
    while this_size < last_size:
        last_size = this_size
        ranges = simplify_ranges(ranges)
        this_size = len(ranges)

    return ranges


def total_ids_inside(ranges: list[tuple[int, int]]) -> int:
    total = 0
    for start_id, end_id in ranges:
        total += end_id - start_id + 1

    return total


def solve(s: str) -> int:
    ranges = find_ranges(s)
    fresh_ids = find_fresh_ingredient_ids(ranges)
    clean_ids = de_overlap_ranges(fresh_ids)
    total = total_ids_inside(clean_ids)
    return total


if __name__ == "__main__":
    with open("day5/input.txt") as file:
        s = file.read()

    num_fresh_ids = solve(s)
    print(num_fresh_ids)
