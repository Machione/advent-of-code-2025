from .puzzle2 import count_removed_rolls, input_to_array

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
    expected = [
        [
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
        ],
        [
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
        ],
        [
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
        ],
        [
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
        ],
        [
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
        ],
        [
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
        ],
        [
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
        ],
        [
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
        ],
        [
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
        ],
        [
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
        ],
    ]
    actual = input_to_array(test_grid)
    assert actual == expected


def test_count_removed_rolls() -> None:
    array = input_to_array(test_grid)
    expected = 43
    actual = count_removed_rolls(array)
    assert actual == expected
