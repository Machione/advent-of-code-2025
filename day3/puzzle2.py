from functools import cache


class Bank:
    def __init__(self, batteries: str) -> None:
        self.batteries = tuple(int(battery) for battery in batteries)
        self.number_of_digits = 12

    def nth_digit(self, n: int) -> int:
        if n > self.number_of_digits:
            raise IndexError()

        index_limit = n - self.number_of_digits
        batteries_remaining = self.batteries_left_after(n - 1)

        if index_limit == 0:
            index_limit = len(batteries_remaining)

        batteries_to_consider = batteries_remaining[:index_limit]
        return max(batteries_to_consider)

    @cache
    def batteries_left_after(self, n: int) -> tuple[int, ...]:
        if n == 0:
            return self.batteries

        n_digit = self.nth_digit(n)
        batteries_considered = self.batteries_left_after(n - 1)
        n_digit_index = batteries_considered.index(n_digit)
        batteries_remaining_after = batteries_considered[n_digit_index + 1 :]
        return batteries_remaining_after

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
