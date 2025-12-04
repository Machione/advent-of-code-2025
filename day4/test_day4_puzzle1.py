from .puzzle1 import count_free_rolls, input_to_array

test_grid = """
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.
"""


def test_input_to_array() -> None:
    expected = (
        (
            0,
            0,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
        ),
        (
            1,
            1,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            1,
        ),
        (
            1,
            1,
            1,
            1,
            1,
            0,
            1,
            0,
            1,
            1,
        ),
        (
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            0,
            1,
            0,
        ),
        (
            1,
            1,
            0,
            1,
            1,
            1,
            1,
            0,
            1,
            1,
        ),
        (
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
            1,
        ),
        (
            0,
            1,
            0,
            1,
            0,
            1,
            0,
            1,
            1,
            1,
        ),
        (
            1,
            0,
            1,
            1,
            1,
            0,
            1,
            1,
            1,
            1,
        ),
        (
            0,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            0,
        ),
        (
            1,
            0,
            1,
            0,
            1,
            1,
            1,
            0,
            1,
            0,
        ),
    )
    actual = input_to_array(test_grid)
    assert actual == expected


def test_count_free_rolls() -> None:
    array = input_to_array(test_grid)
    expected = 13
    actual = count_free_rolls(array)
    assert actual == expected
