import pytest

from .puzzle1 import Bank


@pytest.mark.parametrize(
    "batteries,expected",
    [
        ("987654321111111", 98),
        ("811111111111119", 89),
        ("234234234234278", 78),
        ("818181911112111", 92),
    ],
)
def test_maximum_joltage(batteries: str, expected: int) -> None:
    bank = Bank(batteries)
    actual = bank.maximum_joltage
    assert actual == expected
