# from functools import cache


class Bank:
    def __init__(self, batteries: str) -> None:
        self.batteries = [int(battery) for battery in batteries]
        self.number_of_digits = 12
        self.returned_n = []

    # @cache
    def batteries_to_consider(self, n: int) -> list[int]:
        if n > self.number_of_digits:
            raise IndexError()

        index_limit = n - self.number_of_digits

        if n == 1:
            return self.batteries[:index_limit]

        previously_considered = self.batteries_to_consider(n - 1)

        previously_selected = self.nth_digit(n - 1)
        previously_selected_index = previously_considered.index(previously_selected)
        now_available = previously_considered[previously_selected_index + 1 :]

        newly_available_battery = self.batteries[index_limit]
        now_available.append(newly_available_battery)
        return now_available

    def nth_digit(self, n: int) -> int:
        if n not in self.returned_n:
            print(f"n={n}: Max of {self.batteries_to_consider(n)}")
            self.returned_n.append(n)

        return max(self.batteries_to_consider(n))

    @property
    def maximum_joltage(self) -> int:
        selected_batteries = tuple(
            str(self.nth_digit(n + 1)) for n in range(self.number_of_digits)
        )
        combined_batteries = "".join(selected_batteries)
        return int(combined_batteries)


if __name__ == "__main__":
    total = 0
    with open("day3/input.txt") as file:
        for line in file:
            bank = Bank(line.strip())
            total += bank.maximum_joltage

    print(total)
