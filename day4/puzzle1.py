def input_to_array(grid: str) -> tuple[tuple[int, ...], ...]:
    transformed_grid = tuple(
        tuple(int(c) for c in line.strip().replace(".", "0").replace("@", "1"))
        for line in grid.split()
        if len(line.strip()) > 0
    )
    return transformed_grid


def get_neighbours(
    array: tuple[tuple[int, ...], ...], x_y_index: tuple[int, int]
) -> list[int]:
    x_selected, y_selected = x_y_index
    max_x_exclusive = len(array[0])
    max_y_exclusive = len(array)

    neighbours = []
    for x in range(max(0, x_selected - 1), min(max_x_exclusive, x_selected + 2)):
        for y in range(max(0, y_selected - 1), min(max_y_exclusive, y_selected + 2)):
            if x != x_selected or y != y_selected:
                neighbours.append(array[y][x])

    return neighbours


def count_free_rolls(array: tuple[tuple[int, ...], ...]) -> int:
    count = 0
    for x in range(len(array[0])):
        for y in range(len(array)):
            if array[y][x] == 1:
                neighbours = get_neighbours(array, (x, y))
                num_neighbouring_rolls = sum(neighbours)
                if num_neighbouring_rolls < 4:
                    count += 1

    return count


if __name__ == "__main__":
    with open("day4/input.txt") as file:
        grid = file.read()
        array_input = input_to_array(grid)
        free_rolls = count_free_rolls(array_input)

    print(free_rolls)
