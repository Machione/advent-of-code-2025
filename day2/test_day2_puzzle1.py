from .puzzle1 import is_value_valid, find_invalid_values_in_range, sum_invalid_values
import pytest

@pytest.mark.parametrize("v,expected", [("55", False), ("6464", False), ("123123", False), ("", True), ("1", True), ("1234", True)])
def test_is_value_valid(v: str, expected: bool) -> None:
    actual = is_value_valid(v)
    assert actual == expected


@pytest.mark.parametrize("r,expected", [
    ("11-22", [11, 22]),
    ("95-115", [99]),
    ("998-1012", [1010]),
    ("1188511880-1188511890", [1188511885]),
    ("222220-222224", [222222]),
    ("1698522-1698528", []),
    ("446443-446449", [446446]),
    ("38593856-38593862", [38593859]),
    ("565653-565659", []),
    ("824824821-824824827", []),
    ("2121212118-2121212124", [])
])
def test_find_invalid_values_in_range(r: str, expected: list[int]) -> None:
    actual = find_invalid_values_in_range(r)
    for invalid_value in expected:
        assert invalid_value in actual
    
    assert len(actual) == len(expected)

@pytest.mark.parametrize("ranges,expected", 
    [(['11-22', '95-115', '998-1012', '1188511880-1188511890', '222220-222224', '1698522-1698528', '446443-446449', '38593856-38593862', '565653-565659', '824824821-824824827', '2121212118-2121212124'], 1227775554)]
)
def test_sum_invalid_values(ranges: list[str], expected: int) -> None:
    actual = sum_invalid_values(ranges)
    assert actual == expected