import numpy
import pandas
import pytest

from .puzzle1 import get_numbers, get_operations, solve, solve_columns


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
    expected = pandas.DataFrame(
        ((123, 328, 51, 64), (45, 64, 387, 23), (6, 98, 215, 314))
    )
    actual = get_numbers(test_path)
    assert actual.equals(expected)


def test_get_operations(test_path: str) -> None:
    expected = ("*", "+", "*", "+")
    actual = get_operations(test_path)
    assert actual == expected


def test_solve_columns(test_path: str) -> None:
    expected = [
        numpy.int64(33210),
        numpy.int64(490),
        numpy.int64(4243455),
        numpy.int64(401),
    ]
    actual = solve_columns(test_path)
    assert actual == expected


def test_solve(test_path: str) -> None:
    expected = 4277556
    actual = solve(test_path)
    assert actual == expected
