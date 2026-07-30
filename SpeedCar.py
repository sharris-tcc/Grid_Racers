from Car import Car, moveInRange, spaceAvailable


class SpeedCar(Car):

    def __init__(self, car_id: str):
        super().__init__(car_id)

    def move(self, track):
        bestWeight = 9999
        rowIncrease = 0
        colIncrease = 0
        newRow = 0
        newCol = 0
        distance = 0
        for row in range(-(self.get_row_velocity()), self.get_row_velocity() + 1):
            for col in range(-(self.get_col_velocity()), self.get_col_velocity() + 1):
                if moveInRange(self.get_row() + row, self.get_col() + col, track):
                    if (track.get_weight(self.get_row() + row, self.get_col() + col) <= bestWeight
                            or track.get_weight(self.get_row() + row, self.get_col() + col) == bestWeight
                            and abs(row) + abs(col) > distance)\
                            and spaceAvailable(self.get_row() + row, self.get_col() + col, track):
                        newRow = self.get_row() + row
                        newCol = self.get_col() + col
                        bestWeight = track.get_weight(newRow, newCol)
                        rowIncrease = row
                        colIncrease = col
                        distance = abs(row) + abs(col)
        if self.is_path_clear(track,
                              self.get_row(), self.get_col(),
                              newRow, newCol):
            self.update_car_info(track, rowIncrease, colIncrease)
        else:
            self.complete_collision(track)
