from HandleCar import HandleCar
from SpeedCar import SpeedCar
from Racetrack import Racetrack
from UserCar import UserCar


def selectTrack():
    for x in range(6):
        print(f"track {x + 1}...........press {x + 1}")
    print(f"custom track......press 7")
    option = int(input("Select Option: "))
    if option == 7:
        return "trackCustom.txt"
    else:
        return f"track{option}.txt"


if __name__ == "__main__":
