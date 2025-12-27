from __future__ import annotations

import itertools
from collections import Counter
from collections.abc import Iterator, Sequence
from typing import Optional

# x-axis: Left to right = less to more
# y-axis: Top to bottom = less to more


class Rectangle:
    def __init__(self, p1: tuple[int, int], p2: tuple[int, int]) -> None:
        self.bottom = max(p1[1], p2[1])
        self.top = min(p1[1], p2[1])
        self.left = min(p1[0], p2[0])
        self.right = max(p1[0], p2[0])

    @property
    def area(self) -> int:
        width = self.right - self.left + 1
        height = self.bottom - self.top + 1
        area = width * height
        return area

    def iter_corners(self) -> Iterator[tuple[int, int]]:
        yield (self.left, self.top)
        yield (self.right, self.top)
        yield (self.right, self.bottom)
        yield (self.left, self.bottom)

    def iter_edges(self) -> Iterator[tuple[int, int]]:
        for x in range(self.left, self.right):
            yield (x, self.top)

        for y in range(self.top, self.bottom):
            yield (self.right, y)

        for x in range(self.right, self.left, -1):
            yield (x, self.bottom)

        for y in range(self.bottom, self.top, -1):
            yield (self.left, y)

    def iter_points(self) -> Iterator[tuple[int, int]]:
        for y in range(self.top, self.bottom + 1):
            for x in range(self.left, self.right + 1):
                yield (x, y)


class Line:
    def __init__(self, p1: tuple[int, int], p2: tuple[int, int]) -> None:
        self.p1 = p1
        self.p2 = p2

        self.bottom = max(p1[1], p2[1])
        self.top = min(p1[1], p2[1])
        self.left = min(p1[0], p2[0])
        self.right = max(p1[0], p2[0])

        self.horizontal = self.top == self.bottom
        self.vertical = self.left == self.right
        if self.horizontal is False and self.vertical is False:
            raise NotImplementedError("Only horizontal or vertical lines allowed")

    def extended_point_crosses_at(
        self, point: tuple[int, int]
    ) -> Optional[tuple[int, int]]:
        if self.horizontal:
            # The line is left-to-right, and points on the boundary count as inside
            return None

        if point[0] >= self.right:
            # The point is already to the right of the line
            return None

        if point[1] < self.top or point[1] >= self.bottom:
            # The point misses the ends of the line
            return None

        return (self.left, point[1])

    def __iter__(self):
        if self.horizontal:
            self.current = (self.left, self.top)
            self.end = (self.right, self.top)
            return self

        self.current = (self.left, self.top)
        self.end = (self.left, self.bottom)
        return self

    def __next__(self) -> tuple[int, int]:
        if self.horizontal and self.current[0] > self.end[0]:
            raise StopIteration

        if self.vertical and self.current[1] > self.end[1]:
            raise StopIteration

        this = self.current

        if self.horizontal:
            self.current = (self.current[0] + 1, self.current[1])

        if self.vertical:
            self.current = (self.current[0], self.current[1] + 1)

        return this


class Polygon:
    def __init__(self, points: Sequence[tuple[int, int]]) -> None:
        points = list(points) + [points[0]]
        self.lines = tuple(
            Line(points[i], points[i + 1]) for i in range(len(points) - 1)
        )
        self.boundary = set(point for line in self.lines for point in line)

    def is_inside(self, point: tuple[int, int]) -> bool:
        if point in self.boundary:
            return True

        crossing_points = tuple(
            line.extended_point_crosses_at(point) for line in self.lines
        )
        non_overlapping_crossings = tuple(
            p for p, n in Counter(crossing_points).items() if n == 1 and p is not None
        )
        return bool(len(non_overlapping_crossings) % 2)


def data_to_points(data: str) -> list[tuple[int, int]]:
    points = []
    for line in data.split():
        x, y = line.split(",")
        points.append((int(x), int(y)))

    return points


def all_rectangles_biggest_to_smallest(
    points: list[tuple[int, int]],
) -> list[Rectangle]:
    rects = [
        Rectangle(p1, p2)
        for p1, p2 in itertools.permutations(points, 2)
        if p1[0] <= p2[0] and p1[1] <= p2[1] and (p1[0] < p2[0] or p1[1] < p2[1])
    ]
    rects.sort(key=lambda x: x.area, reverse=True)
    return rects


def solve(data: str) -> int:
    points = data_to_points(data)
    poly = Polygon(points)
    rectangles = all_rectangles_biggest_to_smallest(points)
    for rect in rectangles:
        rect_ok = True
        if rect_ok:
            for p in rect.iter_corners():
                if poly.is_inside(p) is False:
                    rect_ok = False
                    break

        if rect_ok:
            for p in rect.iter_edges():
                if poly.is_inside(p) is False:
                    rect_ok = False
                    break

        if rect_ok:
            for p in rect.iter_points():
                if poly.is_inside(p) is False:
                    rect_ok = False
                    break

        if rect_ok:
            return rect.area

    return 0


if __name__ == "__main__":
    with open("day9/input.txt") as f:
        points_data = f.read()

    print(solve(points_data))
