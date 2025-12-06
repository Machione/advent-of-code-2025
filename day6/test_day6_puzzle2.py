import pytest

from .puzzle2 import (
    collapse,
    get_numbers,
    get_operations,
    numbers_to_columns,
    solve,
)


@pytest.fixture
def test_path(tmpdir) -> str:
    fp = tmpdir.join("testfile.txt")
    test_data = """123 328  51 64 
 45 64  387 23 
  6 98  215 314
*   +   *   +  """
    fp.write(test_data)
    return str(fp)


def test_get_numbers(test_path: str) -> None:
    expected = [
        ("1", "2", "3", " ", "3", "2", "8", " ", " ", "5", "1", " ", "6", "4", " "),
        (" ", "4", "5", " ", "6", "4", " ", " ", "3", "8", "7", " ", "2", "3", " "),
        (" ", " ", "6", " ", "9", "8", " ", " ", "2", "1", "5", " ", "3", "1", "4"),
    ]
    actual = get_numbers(test_path)
    assert actual == expected


def test_numbers_to_columns(test_path: str) -> None:
    expected = [
        [("1", " ", " "), ("2", "4", " "), ("3", "5", "6")],
        [("3", "6", "9"), ("2", "4", "8"), ("8", " ", " ")],
        [(" ", "3", "2"), ("5", "8", "1"), ("1", "7", "5")],
        [("6", "2", "3"), ("4", "3", "1"), (" ", " ", "4")],
    ]
    test_numbers = get_numbers(test_path)
    actual = numbers_to_columns(test_numbers)
    assert actual == expected


def test_get_operations(test_path: str) -> None:
    expected = ("*", "+", "*", "+")
    actual = get_operations(test_path)
    assert actual == expected


@pytest.mark.parametrize(
    "column,expected",
    [
        (
            [("1", " ", " "), ("2", "4", " "), ("3", "5", "6")],
            (1, 24, 356),
        ),
        (
            [("3", "6", "9"), ("2", "4", "8"), ("8", " ", " ")],
            (369, 248, 8),
        ),
        (
            [(" ", "3", "2"), ("5", "8", "1"), ("1", "7", "5")],
            (32, 581, 175),
        ),
        (
            [("6", "2", "3"), ("4", "3", "1"), (" ", " ", "4")],
            (623, 431, 4),
        ),
        (
            [("1", " ", " "), ("2", "4", " "), ("3", "5", "6")],
            (1, 24, 356),
        ),
        (
            [("3", "6", "9"), ("2", "4", "8"), ("8", " ", " ")],
            (369, 248, 8),
        ),
        (
            [(" ", "3", "2"), ("5", "8", "1"), ("1", "7", "5")],
            (32, 581, 175),
        ),
        (
            [("6", "2", "3"), ("4", "3", "1"), (" ", " ", "4")],
            (623, 431, 4),
        ),
    ],
)
def test_collapse(
    column: list[tuple[str, ...]],
    expected: tuple[int, ...],
) -> None:
    actual = collapse(column)
    assert actual == expected


def test_solve(test_path: str) -> None:
    expected = 3263827
    actual = solve(test_path)
    assert actual == expected
