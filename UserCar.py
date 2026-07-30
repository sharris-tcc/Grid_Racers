from Car import Car


class UserCar(Car):

    def __init__(self, car_id: str):
        super().__init__(car_id)

    def move(self, track):
        while True:
            row = int(input(f"Enter row (-{self.get_row_velocity()} - {self.get_row_velocity()}): "))
            if row > self.get_row_velocity() or row < -1 * self.get_row_velocity():
                print(f"{row} is out of range....")
                continue
            else:
                break

        while True:
            col = int(input(f"Enter column (-{self.get_col_velocity()} - {self.get_col_velocity()}): "))
            if col > self.get_col_velocity() or col < -1 * self.get_col_velocity():
                print(f"{col} is out of range....")
                continue
            else:
                break

        moveValid = self.is_path_clear(track,
                                       self.get_row(),
                                       self.get_col(),
                                       self.get_row() + row,
                                       self.get_col() + col)
        if moveValid:
            self.update_car_info(track, row, col)
        else:
            self.complete_collision(track)
