import itertools
from collections import Counter
from collections.abc import Sequence

# x-axis: Left to right = less to more
# y-axis: Top to bottom = less to more


def polygon_lines(
    points: Sequence[tuple[int, int]],
) -> tuple[tuple[tuple[int, int], tuple[int, int]], ...]:
    points = list(points) + [points[0]]
    lines = tuple((points[i], points[i + 1]) for i in range(len(points) - 1))
    return lines


def split_and_clean_polygon_lines(
    lines: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
) -> tuple[
    tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    tuple[tuple[tuple[int, int], tuple[int, int]], ...],
]:
    horizontal_lines: list[tuple[tuple[int, int], tuple[int, int]]] = []
    vertical_lines: list[tuple[tuple[int, int], tuple[int, int]]] = []
    for line in lines:
        if line[0][1] == line[1][1]:
            start = (min(line[0][0], line[1][0]), line[0][1])
            end = (max(line[0][0], line[1][0]), line[0][1])
            horizontal_lines.append((start, end))
        elif line[0][0] == line[1][0]:
            start = (line[0][0], min(line[0][1], line[1][1]))
            end = (line[0][0], max(line[0][1], line[1][1]))
            vertical_lines.append((start, end))

    return tuple(horizontal_lines), tuple(vertical_lines)


def point_inside_polygon(
    horizontal_lines: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    vertical_lines: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    point: tuple[int, int],
) -> bool:
    x, y = point

    colinear_horizontals = (line for line in horizontal_lines if line[0][1] == y)
    for h_line in colinear_horizontals:
        if x >= h_line[0][0] and x <= h_line[1][0]:
            # The point lies on the line
            return True

    colinear_verticals = (line for line in vertical_lines if line[0][0] == x)
    for v_line in colinear_verticals:
        if y >= v_line[0][1] and y <= v_line[1][1]:
            # The point lies on the line
            return True

    crossings_to_right: list[tuple[int, int]] = []
    verticals_to_right = (line for line in vertical_lines if line[0][0] > x)
    for line in verticals_to_right:
        if y >= line[0][1] and y < line[1][1]:
            crossing_point = (line[0][0], y)
            crossings_to_right.append(crossing_point)

    non_overlapping_crossings = tuple(
        p for p, n in Counter(crossings_to_right).items() if n == 1
    )
    return bool(len(non_overlapping_crossings) % 2)


def data_to_points(data: str) -> list[tuple[int, int]]:
    points = []
    for line in data.split():
        x, y = line.split(",")
        points.append((int(x), int(y)))

    return points


def rectangle_area(rectangle: tuple[tuple[int, int], tuple[int, int]]) -> int:
    top_left, bottom_right = rectangle
    top_right = (bottom_right[0], top_left[1])
    bottom_left = (top_left[0], bottom_right[1])
    this_width = top_right[0] - top_left[0] + 1
    this_height = bottom_left[1] - top_left[1] + 1
    this_area = this_width * this_height
    return this_area


def all_rectangles(
    points: list[tuple[int, int]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    rects = [
        (p1, p2)
        for p1, p2 in itertools.permutations(points, 2)
        if p1[0] <= p2[0] and p1[1] <= p2[1] and (p1[0] < p2[0] or p1[1] < p2[1])
    ]
    rects.sort(key=lambda x: rectangle_area(x), reverse=True)
    return rects


def rectangle_ok(
    horizontal_lines: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    vertical_lines: tuple[tuple[tuple[int, int], tuple[int, int]], ...],
    rectangle: tuple[tuple[int, int], tuple[int, int]],
) -> bool:
    top_left, bottom_right = rectangle
    bottom_left = (top_left[0], bottom_right[1])
    if point_inside_polygon(horizontal_lines, vertical_lines, bottom_left) is False:
        return False

    top_right = (bottom_right[0], top_left[1])
    if point_inside_polygon(horizontal_lines, vertical_lines, top_right) is False:
        return False

    all_points = itertools.product(
        range(top_left[0], top_right[0] + 1), range(top_left[1], bottom_left[1] + 1)
    )
    for point in all_points:
        if point_inside_polygon(horizontal_lines, vertical_lines, point) is False:
            return False

    return True


def solve(data: str) -> int:
    points = data_to_points(data)
    print("Read in the data")
    poly = polygon_lines(points)
    print("Converted points to lines on a polygon")
    h_lines, v_lines = split_and_clean_polygon_lines(poly)
    print("Cleaned and categorised lines of polygon")
    rectangles = all_rectangles(points)
    print("Found and sorted all the possible rectangles")
    num_rectangles = len(rectangles)
    for i, rectangle in enumerate(rectangles):
        if rectangle_ok(h_lines, v_lines, rectangle):
            best_area = rectangle_area(rectangle)
            print(
                f"Rectangle [{rectangle[0]}, {rectangle[1]}] with area {best_area} fits!"
            )
            return best_area

        print(
            f"Rectangle {i} of {num_rectangles}, [{rectangle[0]}, {rectangle[1]}] failed"
        )

    return 0


if __name__ == "__main__":
    with open("day9/input.txt") as f:
        points_data = f.read()

    print(solve(points_data))
