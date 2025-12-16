from .puzzle2 import solve

test_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""


def test_solve() -> None:
    expected = 24
    actual = solve(test_data)
    assert actual == expected
