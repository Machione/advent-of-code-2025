class Dial():

    def __init__(self) -> None:
        self.position = 50
        self.points_at_zero_count = 0
        self.passes_zero_count = 0
    
    def tick_left(self) -> None:
        self.position -= 1
        if self.position < 0:
            self.position = 99
    
    def tick_right(self) -> None:
        self.position += 1
        if self.position > 99:
            self.position = 0
    
    def rotate(self, rotation: str) -> None:
        number = int(rotation[1:])

        if rotation.startswith("L"):
            func = self.tick_left
        else:
            func = self.tick_right
        
        for _ in range(number):
            func()
            if self.position == 0:
                self.passes_zero_count += 1
        
        if self.position == 0:
            self.points_at_zero_count += 1


if __name__ == "__main__":
    dial = Dial()
    with open("day1/input.txt") as file:
        for line in file:
            dial.rotate(line.strip())
    
    print(dial.passes_zero_count)