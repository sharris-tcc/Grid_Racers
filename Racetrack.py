class Racetrack:
    def __init__(self):
        self.track = []
        self.weights = []

    def read(self, file):
        with open(file, "r") as f:
            for line in f:
                row = list(line.strip())
                self.track.append(row)
        self.initWeights()

    def initWeights(self):
        for r in range(len(self.track)):
            row = []
            for c in range(len(self.track[r])):
                if self.track[r][c] == 'T':
                    row.append(-1)
                elif self.track[r][c] == 'X':
                    row.append(9999)
                elif self.track[r][c] == 'F':
                    row.append(0)
            self.weights.append(row)

        weight = 0
        update = True
        while update:
            update = False
            for r in range(len(self.weights)):
                for c in range(len(self.weights[r])):
                    if self.weights[r][c] == weight:
                        for v in range(-1, 2):
                            for h in range(-1, 2):
                                if self.weights[v + r][h + c] < 0:
                                    self.weights[v + r][h + c] = weight + 1
                                    update = True
            weight += 1

    def display(self):
        for r in range(len(self.track)):
            for c in range(len(self.track[r])):
                if self.track[r][c] == 'T':
                    print(' ', end="\t")
                else:
                    print(self.track[r][c], end="\t")
            print()
        print("\n")

    def displayWeights(self):
        print(f"\nDimensions {self.rowCount()} x {self.colCount()}")
        for r in range(len(self.weights)):
            for c in range(len(self.weights[r])):
                if self.track[r][c] == 'X':
                    print(self.track[r][c], end="\t")
                else:
                    print(self.weights[r][c], end="\t")
            print()
        print("\n")

    def rowCount(self):
        return len(self.track)

    def colCount(self):
        return len(self.track[0])

    def get_track(self, row, col):
        return self.track[row][col]

    def set_track(self, row, col, value):
        self.track[row][col] = value

    def get_weight(self, row, col):
        return self.weights[row][col]

    def show_banner(self):
        print(r"""
           ______    ____    ____     ____            ____     ___     ______   ______    ____    _____
          / ____/   / __ \  /  _/    / __ \          / __ \   /   |   / ____/  / ____/   / __ \  / ___/
         / / __    / /_/ /  / /     / / / /         / /_/ /  / /| |  / /      / __/     / /_/ / \__ \  
        / /_/ /   / _, _/  / /     / /_/ /         / _, _/  / ___ | / /___   / /___    / _, _/ ___/ /  
        \____/   /_/ |_|  \___/   /_____/         /_/ |_|  /_/  |_| \____/   \____/   /_/ |_| /____/
        """)
