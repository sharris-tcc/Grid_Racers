from abc import ABC, abstractmethod
from Position import Position


def moveInRange(row, col, track):
    return 0 <= row < track.rowCount() and 0 <= col < track.colCount()


def spaceAvailable(row, col, track):
    return track.get_track(row, col) == 'T' or track.get_track(row, col) == 'F'


class Car(ABC):
    def __init__(self, car_id: str):
        self._id_number = car_id
        self._row = 0
        self._col = 0
        self._row_velocity = 1
        self._col_velocity = 1
        self._max_speed = 5
        self._is_winner = False
        self._weight_position = 0
        self._positions = []  # stack of Position objects

    # ---------- Abstract ----------
    @abstractmethod
    def move(self, track):
        pass

    # ---------- Display ----------
    def display_car_info(self):
        print(
            f"Car ID: {self._id_number} "
            f"Coordinates: {self._row},{self._col} "
            f"Max Speed: {self._max_speed} "
            f"Velocity: {self._row_velocity},{self._col_velocity}"
        )

    # ---------- Setup ----------
    def extract_car(self, track):
        row = col = high_weight = 0

        for i in range(track.rowCount()):
            for j in range(track.colCount()):
                if track.get_track(i, j) == 'T' and track.get_weight(i, j) > high_weight:
                    row, col = i, j
                    high_weight = track.get_weight(i, j)

        track.set_track(row, col, self._id_number)
        self._positions.append(Position(row, col))
        self.update_coordinates(row, col)

    # ---------- Movement ----------

    # ---------- Validation ----------
    def row_speed_valid(self, value: int) -> bool:
        return value <= self._row_velocity and abs(value) <= self._max_speed

    def col_speed_valid(self, value: int) -> bool:
        return value <= self._col_velocity and abs(value) <= self._max_speed

    # ---------- Collisions ----------
    def car_collision(self, track):
        row = self._positions[len(self._positions) - 1].getRow()
        col = self._positions[len(self._positions) - 1].getCol()

        if self._max_speed > 1:
            self._max_speed -= 1
        self._row_velocity = 1
        self._col_velocity = 1
        if track.get_track(row, col) == 'X':
            print(f"Car {self._id_number} hit a wall"
                  f" at space {'(' + str(row) + ',' + str(col) + ')'}")
        else:
            print(f"Car {self._id_number} collided with Car {track.get_track(row, col)}"
                  f" at space {'(' + str(row) + ',' + str(col) + ')'}")

    def complete_collision(self, track):
        self.car_collision(track)
        self._positions.pop()
        track.set_track(self.get_row(), self.get_col(), 'T')
        track.set_track(
            self._positions[len(self._positions) - 1].getRow(),
            self._positions[len(self._positions) - 1].getCol(),
            self.get_id_number()
        )
        self.update_coordinates(self._positions[len(self._positions) - 1].getRow(),
                                self._positions[len(self._positions) - 1].getCol())

    # ---------- Path Checking (Bresenham) ----------
    def is_path_clear(self, track, x1, y1, x2, y2):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while x1 != x2 or y1 != y2:
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

            tile = track.get_track(x1, y1)
            self._positions.append(Position(x1, y1))

            if tile == 'X':
                """if x1 == x2 or y1 == y2:
                    return False
                elif self.check_corners(track,
                                        self._positions[len(self._positions) - 1],
                                        self._positions[len(self._positions) - 2],
                                        x2, y2):
                    return self.is_path_clear(track,
                                              self._positions[len(self._positions) - 1].getRow(),
                                              self._positions[len(self._positions) - 1].getCol(),
                                              x2,
                                              y2)
                else:
                    return False"""
                return False

            elif tile == 'F':
                print(f"CAR {self._id_number} WINS!")
                self._is_winner = True
                while self._positions:
                    pos = self._positions.pop()
                    track.set_track(pos.row, pos.col, self._id_number)
                return True

            elif tile != 'T' and tile != self._id_number:
                return False

        return True

    def check_corners(self, track, curr, prev, dest_row, dest_col):
        row_path = dest_row - prev.getRow()
        col_path = dest_col - prev.getCol()

        if row_path > 0:
            next_row = 1 + prev.getRow()
        else:
            next_row = -1 + prev.getRow()
        if col_path > 0:
            next_col = 1 + prev.getCol()
        else:
            next_col = -1 + prev.getCol()

        if track.get_track(next_row, next_col) != 'T' and track.get_track(next_row, next_col) != 'F':
            return False

        if track.get_track(prev.getRow(), prev.getCol() + col_path) == 'T' or \
                track.get_track(prev.getRow() + row_path, prev.getCol()) == 'T':
            self._positions.pop()
            self._positions.append(Position(next_row, next_col))
            return True
        else:
            return False

    # ---------- Updates ----------
    def set_car_move(self, track):
        track.set_track(self._row, self._col, self._id_number)

    def update_coordinates(self, row, col):
        self._row = row
        self._col = col

    def update_velocity(self, row, col):
        self._row_velocity = min(row, self._max_speed)
        self._col_velocity = min(col, self._max_speed)

    def update_car_info(self, track, row, col):
        row_total = self._row + row
        col_total = self._col + col

        row_total = max(0, min(row_total, track.rowCount() - 1))
        col_total = max(0, min(col_total, track.colCount() - 1))

        track.set_track(self._row, self._col, 'T')
        self.update_coordinates(row_total, col_total)
        self._weight_position = track.get_weight(row_total, col_total)
        self.update_velocity(
            self._row_velocity + abs(row),
            self._col_velocity + abs(col),
        )
        self.set_car_move(track)

    # ---------- Comparison ----------
    def __lt__(self, other):
        return self._weight_position < other.get_weight_position()

    # ---------- Get/Set ----------
    # id_number
    def get_id_number(self):
        return self._id_number

    def set_id_number(self, id_number):
        self._id_number = id_number

    # row
    def get_row(self):
        return self._row

    def set_row(self, row):
        self._row = row

    # col
    def get_col(self):
        return self._col

    def set_col(self, col):
        self._col = col

    # row_velocity
    def get_row_velocity(self):
        return self._row_velocity

    def set_row_velocity(self, row_velocity):
        self._row_velocity = row_velocity

    # col_velocity
    def get_col_velocity(self):
        return self._col_velocity

    def set_col_velocity(self, col_velocity):
        self._col_velocity = col_velocity

    # max_speed
    def get_max_speed(self):
        return self._max_speed

    def set_max_speed(self, max_speed):
        self._max_speed = max_speed

    # is_winner
    def get_is_winner(self):
        return self._is_winner

    def set_is_winner(self, is_winner):
        self._is_winner = is_winner

    # weight_position
    def get_weight_position(self):
        return self._weight_position

    def set_weight_position(self, weight_position):
        self._weight_position = weight_position
