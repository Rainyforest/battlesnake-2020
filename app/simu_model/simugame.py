import time

from basic_model.direction import Direction
from tools.mapper import simu_to_gamestate
from service.snake_controller import SnakeController, ControllerMode
from simu_model.guiboard import GuiBoard


class SimuGame:
    def __init__(self, map_size, number_of_snakes):
        self.map_size = map_size
        self.number_of_snakes = number_of_snakes
        self.board = self.init_board()  # turn in board

    BOARD_SIZE_SMALL = 7
    BOARD_SIZE_MEDIUM = 11
    BOARD_SIZE_LARGE = 19

    def init_board(self):
        board = GuiBoard(self.map_size, self.map_size)
        board.init_snakes(self.number_of_snakes)
        board.init_food(self.number_of_snakes)
        return board

    def reset(self):
        pass

    def play(self):
        controllers = []
        for _ in self.board.snake_list:
            controllers.append(SnakeController(ControllerMode.ALGO))

        while not self.board.decided:
            desired_directions = []
            for i in range(len(self.board.snake_list)):
                if not self.board.snake_list[i].alive():
                    desired_directions.append(Direction.NONE)
                    continue
                gamestate = simu_to_gamestate(self.board, i)
                move = controllers[i].move(gamestate)
                desired_directions.append(move)

            self.board.desired_directions = desired_directions
            self.board.step()
            # print("LENGTH: %d" % self.board.snake_list[0].length)
            # print("DIRECTION: {}".format(self.board.desired_directions))
            # print("BODY LIST: {}".format(self.board.snake_list[0].body_list))
            # print("HEALTH: %d" % self.board.snake_list[0].health)
            # print(self.board)
            self.board.render()
            time.sleep(0.05)
