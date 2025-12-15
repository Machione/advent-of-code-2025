from __future__ import annotations

import itertools
import math
from typing import Any


class Point2D:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point2D):
            return False

        if self.x == other.x and self.y == other.y:
            return True

        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def distance_to(self, other: Point2D) -> float:
        x_diff = abs(self.x - other.x) ** 2
        y_diff = abs(self.y - other.y) ** 2
        dist = math.sqrt(x_diff + y_diff)
        return dist

    def area_covered(self, other: Point2D) -> int:
        left = min(self.x, other.x)
        right = max(self.x, other.x)
        width = right - left + 1

        bottom = min(self.y, other.y)
        top = max(self.y, other.y)
        height = top - bottom + 1

        area = width * height
        return area


def data_to_points(data: str) -> list[Point2D]:
    points = []
    for line in data.split():
        x, y = line.split(",")
        points.append(Point2D(int(x), int(y)))

    return points


def all_areas_biggest_to_smallest(
    points: list[Point2D],
) -> list[tuple[tuple[Point2D, Point2D], int]]:
    distances = [
        ((p1, p2), p1.area_covered(p2)) for p1, p2 in itertools.combinations(points, 2)
    ]
    distances.sort(key=lambda x: x[1], reverse=True)
    return distances


def solve(data: str) -> int:
    points = data_to_points(data)
    areas = all_areas_biggest_to_smallest(points)
    return areas[0][1]


if __name__ == "__main__":
    with open("day9/input.txt") as f:
        points_data = f.read()

    print(solve(points_data))
