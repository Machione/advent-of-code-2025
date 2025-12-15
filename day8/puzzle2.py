from __future__ import annotations

import itertools
import math
from typing import Any


class Point3D:
    def __init__(self, x: int, y: int, z: int) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Point3D):
            return False

        if self.x == other.x and self.y == other.y and self.z == other.z:
            return True

        return False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def distance_to(self, other: Point3D) -> float:
        x_diff = abs(self.x - other.x) ** 2
        y_diff = abs(self.y - other.y) ** 2
        z_diff = abs(self.z - other.z) ** 2
        dist = math.sqrt(x_diff + y_diff + z_diff)
        return dist


class Circuit:
    def __init__(self, junction_box: Point3D) -> None:
        self._junction_boxes = {junction_box}

    def combine(self, other: Circuit) -> None:
        if self != other:
            self._junction_boxes.update(other._junction_boxes)
            other._junction_boxes = set()

    def __len__(self) -> int:
        return len(self._junction_boxes)

    def __contains__(self, junction_box: Point3D) -> bool:
        return junction_box in self._junction_boxes


def data_to_points(data: str) -> list[Point3D]:
    points = []
    for line in data.split():
        x, y, z = line.split(",")
        points.append(Point3D(int(x), int(y), int(z)))

    return points


def all_distances_nearest_to_farthest(
    points: list[Point3D],
) -> list[tuple[tuple[Point3D, Point3D], float]]:
    distances = [
        ((p1, p2), p1.distance_to(p2)) for p1, p2 in itertools.combinations(points, 2)
    ]
    distances.sort(key=lambda x: x[1])
    return distances


def solve(data: str) -> int:
    points = data_to_points(data)
    num_points = len(points)
    distances = all_distances_nearest_to_farthest(points)
    circuits = [Circuit(j) for j in points]

    for boxes, _ in distances:
        j1, j2 = boxes
        j1_circuit = [c for c in circuits if j1 in c][0]
        j2_circuit = [c for c in circuits if j2 in c][0]
        j1_circuit.combine(j2_circuit)

        if any(len(c) == num_points for c in circuits):
            break

    return j1.x * j2.x


if __name__ == "__main__":
    with open("day8/input.txt") as f:
        points_data = f.read()

    print(solve(points_data))
