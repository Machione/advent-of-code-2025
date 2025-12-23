import itertools
from collections.abc import Iterator, Sequence
from functools import cache


class Rectangle:
    def __init__(self, p1: tuple[int, int], p2: tuple[int, int]) -> None:
        self.bottom_y = max(p1[1], p2[1])
        self.top_y = min(p1[1], p2[1])
        self.left_x = min(p1[0], p2[0])
        self.right_x = max(p1[0], p2[0])

    @property
    def area(self) -> int:
        width = self.right_x - self.left_x + 1
        height = self.bottom_y - self.top_y + 1
        area = width * height
        return area

    def iter_corners(self) -> Iterator[tuple[int, int]]:
        yield (self.left_x, self.top_y)
        yield (self.right_x, self.top_y)
        yield (self.right_x, self.bottom_y)
        yield (self.left_x, self.bottom_y)

    def iter_edges(self) -> Iterator[tuple[int, int]]:
        for x in range(self.left_x, self.right_x):
            yield (x, self.top_y)

        for y in range(self.top_y, self.bottom_y):
            yield (self.right_x, y)

        for x in range(self.right_x, self.left_x, -1):
            yield (x, self.bottom_y)

        for y in range(self.bottom_y, self.top_y, -1):
            yield (self.left_x, y)

    def iter_points(self) -> Iterator[tuple[int, int]]:
        for y in range(self.top_y, self.bottom_y + 1):
            for x in range(self.left_x, self.right_x + 1):
                yield (x, y)


class Line:
    def __init__(self, p1: tuple[int, int], p2: tuple[int, int]) -> None:
        self.horizontal = p1[1] == p2[1]
        self.vertical = p1[0] == p2[0]
        if self.horizontal and p1[0] < p2[0]:
            self.p1 = p1
            self.p2 = p2
        elif self.horizontal:
            self.p1 = p2
            self.p2 = p1
        elif self.vertical and p1[1] < p2[1]:
            self.p1 = p1
            self.p2 = p2
        else:
            self.p1 = p2
            self.p2 = p1

    def extended_point_crosses(self, point: tuple[int, int]) -> bool:
        if self.horizontal:
            # The line is left-to-right, and points on the boundary count as inside
            return False

        if point[1] <= self.p1[1] or point[1] >= self.p2[1]:
            # The point misses the ends of the line
            return False

        if point[0] >= self.p1[0]:
            # The point is already to the right of the line
            return False

        return True

    def __iter__(self):
        self.current = self.p1
        self.end = self.p2
        return self

    def __next__(self) -> tuple[int, int]:
        if self.horizontal:
            n = (self.current[0] + 1, self.current[1])
            if n[0] > self.end[0]:
                raise StopIteration

            self.current = n
            return n

        n = (self.current[0], self.current[1] + 1)
        if n[1] > self.end[1]:
            raise StopIteration

        self.current = n
        return n


class Polygon:
    def __init__(self, points: Sequence[tuple[int, int]]) -> None:
        points = list(points) + [points[0]]
        self.lines = tuple(
            Line(points[i], points[i + 1]) for i in range(len(points) - 1)
        )

    @cache
    def is_inside(self, point: tuple[int, int]) -> bool:
        count_crosses = sum(
            int(line.extended_point_crosses(point)) for line in self.lines
        )
        return bool(count_crosses % 2)


class Plot:
    def __init__(self) -> None:
        self._marks: dict[tuple[int, int], str] = {}

    def mark(self, x: int, y: int, marker: str) -> None:
        self._marks[(x, y)] = marker

    def get(self, x: int, y: int) -> str:
        return self._marks.get((x, y), " ")

    def print(self) -> None:
        left = min(p[0] for p, m in self._marks.items() if m == "0")
        right = max(p[0] for p, m in self._marks.items() if m == "0")
        top = min(p[1] for p, m in self._marks.items() if m == "0")
        bottom = max(p[1] for p, m in self._marks.items() if m == "0")
        with open("day9/solution.txt", "w") as f:
            for y in range(top, bottom + 1):
                marks_this_line = {p: m for p, m in self._marks.items() if p[1] == y}
                line = "".join(
                    marks_this_line.get((x, y), " ") for x in range(left, right + 1)
                )
                f.write(line + "\n")


def data_to_points(data: str) -> list[tuple[int, int]]:
    points = []
    for line in data.split():
        x, y = line.split(",")
        points.append((int(x), int(y)))

    return points


def all_rectangles_biggest_to_smallest(
    points: list[tuple[int, int]],
) -> list[Rectangle]:
    rects = [Rectangle(p1, p2) for p1, p2 in itertools.combinations(points, 2)]
    rects.sort(key=lambda x: x.area, reverse=True)
    return rects


def solve(data: str) -> int:
    points = data_to_points(data)
    poly = Polygon(points)
    rectangles = all_rectangles_biggest_to_smallest(points)
    for rect in rectangles:
        rect_ok = True
        for p in rect.iter_corners():
            if poly.is_inside(p) is False:
                rect_ok = False
                break

        if rect_ok is False:
            continue

        for p in rect.iter_edges():
            if poly.is_inside(p) is False:
                rect_ok = False
                break

        if rect_ok is False:
            continue

        for p in rect.iter_points():
            if poly.is_inside(p) is False:
                rect_ok = False
                break

        if rect_ok:
            return rect.area

    return 0


def plot_solution(data: str) -> None:
    plot = Plot()

    points = data_to_points(data)
    for p in points:
        plot.mark(p[0], p[1], "•")

    poly = Polygon(points)
    for line in poly.lines:
        for p in line:
            if plot.get(p[0], p[1]) != "•":
                if line.horizontal:
                    plot.mark(p[0], p[1], "-")
                else:
                    plot.mark(p[0], p[1], "|")

    rectangles = all_rectangles_biggest_to_smallest(points)
    for rect in rectangles:
        rect_ok = True
        for p in rect.iter_corners():
            if poly.is_inside(p) is False:
                rect_ok = False
                break

        if rect_ok is False:
            continue

        for p in rect.iter_edges():
            if poly.is_inside(p) is False:
                rect_ok = False
                break

        if rect_ok is False:
            continue

        for p in rect.iter_points():
            if poly.is_inside(p) is False:
                rect_ok = False
                break

        if rect_ok is False:
            continue

        print(rect.area)

        for p in rect.iter_points():
            if plot.get(p[0], p[1]) in (" ", "•"):
                plot.mark(p[0], p[1], "0")

        plot.print()
        break


if __name__ == "__main__":
    test_data = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    plot_solution(test_data)

    with open("day9/input.txt") as f:
        points_data = f.read()

    plot_solution(points_data)
