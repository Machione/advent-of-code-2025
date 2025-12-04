class Bank:
    def __init__(self, batteries: str) -> None:
        self.batteries = [int(battery) for battery in batteries]

    @property
    def first_digit(self) -> int:
        return max(self.batteries[:-1])

    @property
    def second_digit(self) -> int:
        first_digit_index = self.batteries.index(self.first_digit)
        batteries_after = self.batteries[first_digit_index + 1 :]
        return max(batteries_after)

    @property
    def maximum_joltage(self) -> int:
        return int(str(self.first_digit) + str(self.second_digit))


if __name__ == "__main__":
    total = 0
    with open("day3/input.txt") as file:
        for line in file:
            bank = Bank(line.strip())
            total += bank.maximum_joltage

    print(total)
