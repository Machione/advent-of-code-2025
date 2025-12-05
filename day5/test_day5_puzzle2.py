from .puzzle2 import (
    de_overlap_ranges,
    find_fresh_ingredient_ids,
    find_ranges,
    solve,
    total_ids_inside,
)

test_s = """3-5
10-14
16-20
12-18

1
5
8
11
17
32"""


def test_find_ranges():
    expected = ["3-5", "10-14", "16-20", "12-18"]
    actual = find_ranges(test_s)
    assert actual == expected


def test_find_fresh_ingredient_ids():
    expected = [(3, 5), (10, 14), (16, 20), (12, 18)]
    ranges = find_ranges(test_s)
    actual = find_fresh_ingredient_ids(ranges)
    assert actual == expected


def test_de_overlap_ranges():
    expected = [(3, 5), (10, 20)]
    ranges = find_ranges(test_s)
    fresh_ids = find_fresh_ingredient_ids(ranges)
    actual = de_overlap_ranges(fresh_ids)
    assert actual == expected


def test_total_ids_inside():
    expected = 14
    ranges = find_ranges(test_s)
    fresh_ids = find_fresh_ingredient_ids(ranges)
    clean_ids = de_overlap_ranges(fresh_ids)
    actual = total_ids_inside(clean_ids)
    assert actual == expected


def test_solve():
    expected = 14
    actual = solve(test_s)
    assert actual == expected
