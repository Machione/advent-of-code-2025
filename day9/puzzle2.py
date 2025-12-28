from __future__ import annotations

import itertools
import multiprocessing
from collections import Counter
from collections.abc import Iterator, Sequence
from concurrent.futures import ProcessPoolExecutor
from typing import Optional

from tqdm import tqdm

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
        actual_crossing_points = tuple(p for p in crossing_points if p is not None)
        non_overlapping_crossings = tuple(
            p for p, n in Counter(actual_crossing_points).items() if n == 1
        )
        return bool(len(non_overlapping_crossings) % 2)


def data_to_points(data: str) -> list[tuple[int, int]]:
    points = []
    for line in data.split():
        x, y = line.split(",")
        points.append((int(x), int(y)))

    return points


def all_rectangles(
    points: list[tuple[int, int]],
) -> tuple[Rectangle, ...]:
    rects = tuple(
        Rectangle(p1, p2)
        for p1, p2 in itertools.permutations(points, 2)
        if p1[0] <= p2[0] and p1[1] <= p2[1] and (p1[0] < p2[0] or p1[1] < p2[1])
    )
    return rects


def rectangle_ok(
    poly: Polygon,
    rectangle: Rectangle,
    current_max: multiprocessing.sharedctypes.Synchronized,
) -> Optional[Rectangle]:
    if rectangle.area <= current_max.value:
        return None

    for p in rectangle.iter_corners():
        if poly.is_inside(p) is False:
            return None

    for p in rectangle.iter_edges():
        if poly.is_inside(p) is False:
            return None

    for p in rectangle.iter_points():
        if poly.is_inside(p) is False:
            return None

    current_max.value = rectangle.area

    return rectangle


def single_pool_rectangle_ok(args) -> Optional[Rectangle]:
    poly, rectangle, cur = args
    return rectangle_ok(poly, rectangle, cur)


def solve(data: str) -> int:
    points = data_to_points(data)
    poly = Polygon(points)
    rectangles = all_rectangles(points)
    with tqdm(total=len(rectangles)) as progress:
        with multiprocessing.Manager() as manager:
            current_max_size = manager.Value("b", 0)
            last_max_size = 0
            ok_rectangles: list[Rectangle] = []
            args = [(poly, rectangle, current_max_size) for rectangle in rectangles]
            with ProcessPoolExecutor() as executor:
                for res in executor.map(single_pool_rectangle_ok, args):
                    progress.update()
                    if res is not None:
                        ok_rectangles.append(res)

                    if current_max_size.value > last_max_size:
                        print(current_max_size.value)
                        last_max_size = current_max_size.value

    ok_rectangles.sort(key=lambda x: x.area, reverse=True)
    return ok_rectangles[0].area


if __name__ == "__main__":
    multiprocessing.set_start_method("forkserver")
    with open("day9/input.txt") as f:
        points_data = f.read()

    print(solve(points_data))
