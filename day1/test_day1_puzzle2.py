from .puzzle2 import Dial


def test_puzzle2():
    d = Dial()
    assert d.position == 50
    assert d.points_at_zero_count == 0
    assert d.passes_zero_count == 0

    d.rotate("L68")
    assert d.position == 82
    assert d.points_at_zero_count == 0
    assert d.passes_zero_count == 1

    d.rotate("L30")
    assert d.position == 52
    assert d.points_at_zero_count == 0
    assert d.passes_zero_count == 1

    d.rotate("R48")
    assert d.position == 0
    assert d.points_at_zero_count == 1
    assert d.passes_zero_count == 2

    d.rotate("L5")
    assert d.position == 95
    assert d.points_at_zero_count == 1
    assert d.passes_zero_count == 2

    d.rotate("R60")
    assert d.position == 55
    assert d.points_at_zero_count == 1
    assert d.passes_zero_count == 3

    d.rotate("L55")
    assert d.position == 0
    assert d.points_at_zero_count == 2
    assert d.passes_zero_count == 4

    d.rotate("L1")
    assert d.position == 99
    assert d.points_at_zero_count == 2
    assert d.passes_zero_count == 4

    d.rotate("L99")
    assert d.position == 0
    assert d.points_at_zero_count == 3
    assert d.passes_zero_count == 5

    d.rotate("R14")
    assert d.position == 14
    assert d.points_at_zero_count == 3
    assert d.passes_zero_count == 5

    d.rotate("L82")
    assert d.position == 32
    assert d.points_at_zero_count == 3
    assert d.passes_zero_count == 6
