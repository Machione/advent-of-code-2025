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


def find_ingredient_ids(s: str) -> set[int]:
    ids = []
    past_empty_line = False
    for line in s.split():
        clean_line = line.strip()

        if "-" not in clean_line:
            past_empty_line = True

        if past_empty_line is True and len(clean_line) > 0:
            ids.append(int(clean_line))

    return set(ids)


def get_fresh_ids(s: str) -> set[int]:
    ranges = find_ranges(s)
    fresh_id_ranges = find_fresh_ingredient_ids(ranges)
    ids = find_ingredient_ids(s)

    fresh_ids = set()
    for i in ids:
        for fresh_range_start, fresh_range_end in fresh_id_ranges:
            if i >= fresh_range_start and i <= fresh_range_end:
                fresh_ids.add(i)

    return fresh_ids


if __name__ == "__main__":
    with open("day5/input.txt") as file:
        s = file.read()

    fresh_ids = get_fresh_ids(s)
    print(len(fresh_ids))
