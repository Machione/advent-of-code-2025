def input_to_array(grid: str) -> list[list[int]]:
    transformed_grid = [
        [int(c) for c in line.strip().replace(".", "0").replace("@", "1")]
        for line in grid.split()
        if len(line.strip()) > 0
    ]
    return transformed_grid


def get_neighbours(array: list[list[int]], x_y_index: tuple[int, int]) -> list[int]:
    x_selected, y_selected = x_y_index
    max_x_exclusive = len(array[0])
    max_y_exclusive = len(array)

    neighbours = []
    for x in range(max(0, x_selected - 1), min(max_x_exclusive, x_selected + 2)):
        for y in range(max(0, y_selected - 1), min(max_y_exclusive, y_selected + 2)):
            if x != x_selected or y != y_selected:
                neighbours.append(array[y][x])

    return neighbours


def remove_free_rolls(array: list[list[int]]) -> list[list[int]]:
    for x in range(len(array[0])):
        for y in range(len(array)):
            if array[y][x] == 1:
                neighbours = get_neighbours(array, (x, y))
                num_neighbouring_rolls = sum(neighbours)
                if num_neighbouring_rolls < 4:
                    array[y][x] = 0

    return array


def count_removed_rolls(array: list[list[int]]) -> int:
    number_removed = 0
    rolls_remaining_last_time = sum(sum(row) for row in array)

    array = remove_free_rolls(array)
    rolls_remaining = sum(sum(row) for row in array)
    rolls_removed = rolls_remaining_last_time - rolls_remaining
    number_removed += rolls_removed

    while rolls_removed > 0:
        rolls_remaining_last_time = rolls_remaining
        array = remove_free_rolls(array)
        rolls_remaining = sum(sum(row) for row in array)
        rolls_removed = rolls_remaining_last_time - rolls_remaining
        number_removed += rolls_removed

    return number_removed


if __name__ == "__main__":
    with open("day4/input.txt") as file:
        grid = file.read()

    array_input = input_to_array(grid)
    removed_rolls = count_removed_rolls(array_input)
    print(removed_rolls)
