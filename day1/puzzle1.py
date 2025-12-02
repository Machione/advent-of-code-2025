class Dial:
    def __init__(self) -> None:
        self.position = 50
        self.points_at_zero_count = 0

    def rotate(self, rotation: str) -> None:
        number = int(rotation[1:])
        if rotation.startswith("L"):
            number *= -1

        self.position += number

        while self.position < 0:
            self.position += 100

        while self.position > 99:
            self.position -= 100

        if self.position == 0:
            self.points_at_zero_count += 1


if __name__ == "__main__":
    dial = Dial()
    with open("day1/input.txt") as file:
        for line in file:
            dial.rotate(line.strip())

    print(dial.points_at_zero_count)
