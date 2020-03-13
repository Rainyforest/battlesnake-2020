class Board:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.food_list = []
        self.snake_list = []


    @staticmethod
    def neighbors(a):
        (x, y) = a
        return [
            (x, y - 1),
            (x - 1, y),
            (x, y + 1),
            (x + 1, y)
        ]

    def is_obstacle(self, coord):
        (x, y) = coord
        w = self.width
        h = self.height
        if x < 0 or x > w - 1:
            return True
        if y < 0 or y > h - 1:
            return True
        if not (self.board_map()[y][x] == 0 or self.board_map()[y][x] == "f"):
            return True
        return False

    # get if two coords are connected and dist btw them
    def get(self, a, b):
        if (self.is_obstacle(a)) or self.is_obstacle(b):
            return 0
        if abs(a[0] - b[0]) == 1 and a[1] == b[1]:
            return 1
        if abs(a[1] - b[1]) == 1 and a[0] == b[0]:
            return 1
        return 0

    def board_map(self):
        # initiate an empty board, 0 means empty space
        board_map = []

        for row in range(0, self.height):
            board_row = []
            for col in range(0, self.width):
                board_row.append(0)
            board_map.append(board_row)

        # insert food coordinates, and replace 0 with f indicates food
        for food in self.food_list:
            x = food[0]
            y = food[1]
            board_map[y][x] = "f"

        # insert snake coordinates to the board, snake 1's body number is 1, etc
        k = 1
        for snake in self.snake_list:
            for body in snake.body_list:
                x = body[0]
                y = body[1]
                board_map[y][x] = k
            k += 1

        return board_map

