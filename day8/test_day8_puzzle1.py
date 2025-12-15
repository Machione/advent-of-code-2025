import math

import pytest

from .puzzle1 import Point3D, all_distances_nearest_to_farthest, data_to_points, solve

test_data = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689"""


@pytest.mark.parametrize(
    "x,y,z",
    [
        (162, 817, 812),
        (57, 618, 57),
        (906, 360, 560),
        (592, 479, 940),
        (352, 342, 300),
        (466, 668, 158),
        (542, 29, 236),
        (431, 825, 988),
        (739, 650, 466),
        (52, 470, 668),
        (216, 146, 977),
        (819, 987, 18),
        (117, 168, 530),
        (805, 96, 715),
        (346, 949, 466),
        (970, 615, 88),
        (941, 993, 340),
        (862, 61, 35),
        (984, 92, 344),
        (425, 690, 689),
    ],
)
def test_point_3d(x: int, y: int, z: int) -> None:
    point = Point3D(x, y, z)
    assert point.x == x
    assert point.y == y
    assert point.z == z


@pytest.mark.parametrize(
    "p1,p2,expected",
    [
        (Point3D(425, 690, 689), Point3D(425, 690, 689), True),
        (Point3D(425, 690, 689), Point3D(425, 690, 688), False),
    ],
)
def test_point_3d_equality(p1: Point3D, p2: Point3D, expected: bool) -> None:
    p1_equals_p2 = p1 == p2
    assert p1_equals_p2 == expected
    p2_equals_p1 = p2 == p1
    assert p2_equals_p1 == expected


@pytest.mark.parametrize(
    "p1,p2",
    [
        (Point3D(425, 690, 689), Point3D(425, 690, 689)),
        (Point3D(425, 690, 689), Point3D(425, 690, 688)),
    ],
)
def test_point_3d_hash(p1: Point3D, p2: Point3D) -> None:
    expected = p1 == p2
    actual = hash(p1) == hash(p2)
    assert expected == actual


@pytest.mark.parametrize(
    "p1,p2,expected",
    [(Point3D(162, 817, 812), Point3D(57, 618, 57), math.sqrt(620651))],
)
def test_distance_to(p1: Point3D, p2: Point3D, expected: float) -> None:
    actual = p1.distance_to(p2)
    assert actual == expected

    actual = p2.distance_to(p1)
    assert actual == expected


def test_data_to_points() -> None:
    expected = [
        Point3D(162, 817, 812),
        Point3D(57, 618, 57),
        Point3D(906, 360, 560),
        Point3D(592, 479, 940),
        Point3D(352, 342, 300),
        Point3D(466, 668, 158),
        Point3D(542, 29, 236),
        Point3D(431, 825, 988),
        Point3D(739, 650, 466),
        Point3D(52, 470, 668),
        Point3D(216, 146, 977),
        Point3D(819, 987, 18),
        Point3D(117, 168, 530),
        Point3D(805, 96, 715),
        Point3D(346, 949, 466),
        Point3D(970, 615, 88),
        Point3D(941, 993, 340),
        Point3D(862, 61, 35),
        Point3D(984, 92, 344),
        Point3D(425, 690, 689),
    ]
    actual = data_to_points(test_data)
    assert actual == expected


def test_all_distances_nearest_to_farthest() -> None:
    points = data_to_points(test_data)
    actual = all_distances_nearest_to_farthest(points)

    expected_nearest = (
        (Point3D(162, 817, 812), Point3D(425, 690, 689)),
        (Point3D(162, 817, 812), Point3D(431, 825, 988)),
        (Point3D(906, 360, 560), Point3D(805, 96, 715)),
        (Point3D(431, 825, 988), Point3D(425, 690, 689)),
    )
    for expected_p1, expected_p2 in expected_nearest:
        actual_p1, actual_p2 = actual.pop(0)[0]
        assert (actual_p1 == expected_p1 and actual_p2 == expected_p2) or (
            actual_p1 == expected_p2 and actual_p2 == expected_p1
        )


def test_solve() -> None:
    expected = 40
    actual = solve(test_data, 10)
    assert actual == expected
