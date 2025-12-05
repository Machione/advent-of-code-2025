from .puzzle1 import (
    find_fresh_ingredient_ids,
    find_ingredient_ids,
    find_ranges,
    get_fresh_ids,
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


def test_ingredient_ids():
    expected = {1, 5, 8, 11, 17, 32}
    actual = find_ingredient_ids(test_s)
    assert actual == expected


def test_get_fresh_ids():
    expected = {5, 11, 17}
    actual = get_fresh_ids(test_s)
    assert actual == expected
