import itertools
from collections.abc import Sequence


class Point2D:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class Rectangle:
    def __init__(self, p1: Point2D, p2: Point2D) -> None:
        self.bottom_y = min(p1.y, p2.y)
        self.top_y = max(p1.y, p2.y)
        self.left_x = min(p1.x, p2.x)
        self.right_x = max(p1.x, p2.x)

    @property
    def area(self) -> int:
        width = self.right_x - self.left_x + 1
        height = self.top_y - self.bottom_y + 1
        area = width * height
        return area

    @property
    def corners(self) -> tuple[Point2D, Point2D, Point2D, Point2D]:
        top_left = Point2D(self.left_x, self.top_y)
        top_right = Point2D(self.right_x, self.top_y)
        bottom_right = Point2D(self.right_x, self.bottom_y)
        bottom_left = Point2D(self.left_x, self.bottom_y)
        return (top_left, top_right, bottom_right, bottom_left)


class Line:
    def __init__(self, p1: Point2D, p2: Point2D) -> None:
        self.p1 = p1
        self.p2 = p2

    def extended_point_crosses(self, point: Point2D) -> bool:
        if self.p1.y == self.p2.y:
            # The line is left-to-right, and points on the boundary count as inside
            return False

        if point.y <= min(self.p1.y, self.p2.y) or point.y >= max(self.p1.y, self.p2.y):
            # The point misses the ends of the line
            return False

        if point.x >= self.p1.x:
            # The point is already to the right of the line
            return False

        return True


class Polygon:
    def __init__(self, points: Sequence[Point2D]) -> None:
        points = list(points) + [points[0]]
        self.lines = tuple(
            Line(points[i], points[i + 1]) for i in range(len(points) - 1)
        )

    def is_inside(self, point: Point2D) -> bool:
        count_crosses = sum(
            int(line.extended_point_crosses(point)) for line in self.lines
        )
        return bool(count_crosses % 2)


def data_to_points(data: str) -> list[Point2D]:
    points = []
    for line in data.split():
        x, y = line.split(",")
        points.append(Point2D(int(x), int(y)))

    return points


def all_rectangles_biggest_to_smallest(
    points: list[Point2D],
) -> list[Rectangle]:
    rects = [Rectangle(p1, p2) for p1, p2 in itertools.combinations(points, 2)]
    rects.sort(key=lambda x: x.area, reverse=True)
    return rects


def solve(data: str) -> int:
    points = data_to_points(data)
    poly = Polygon(points)
    rectangles = all_rectangles_biggest_to_smallest(points)
    for rect in rectangles:
        if all(poly.is_inside(p) for p in rect.corners):
            return rect.area

    return 0


if __name__ == "__main__":
    with open("day9/input.txt") as f:
        points_data = f.read()

    print(solve(points_data))
