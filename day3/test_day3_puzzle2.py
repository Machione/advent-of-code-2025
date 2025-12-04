import pytest

from .puzzle2 import Bank


@pytest.mark.parametrize(
    "batteries,expected",
    [
        ("987654321111111", 987654321111),
        ("811111111111119", 811111111119),
        ("234234234234278", 434234234278),
        ("818181911112111", 888911112111),
    ],
)
def test_maximum_joltage(batteries: str, expected: int) -> None:
    bank = Bank(batteries)
    actual = bank.maximum_joltage
    assert actual == expected
