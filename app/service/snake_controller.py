import os
import random

# import math

import os.path
from enum import Enum

import numpy as np

from basic_model.direction import Direction
from algorithms.search import A_star_search, single_step_direction
from algorithms.problem import BoardProblem
from tools.utils import dist


class ControllerMode(Enum):
    ALGO = 0
    NN = 1


class SnakeController:
    def __init__(self, mode):
        self.board = None
        self.turn = 0  # how many round played
        self.you = None
        self.mode = mode

    def move(self, gamestate):
        self.update_gamestate(gamestate)
        if self.mode == ControllerMode.ALGO:
            return self.algo_decide_next()
        elif self.mode == ControllerMode.NN:
            return self.NN_decide_next()
        else:
            return None

    def update_gamestate(self, gamestate):
        self.board = gamestate.board
        self.turn = gamestate.turn  # how many round played
        self.you = gamestate.you

    def fetch_nearest_food(self, ava_dirs):
        my_snake = self.you
        head = my_snake.head()
        foods = self.board.food_list
        dir_list = ava_dirs

        search_dir = Direction.NONE

        def dist_to_head(e):
            return dist(head, e)

        if foods:
            foods.sort(reverse=False, key=dist_to_head)
            food = foods[0]
            problem = BoardProblem(head, food, self.board)
            path = A_star_search(problem)
            if path:
                search_dir = single_step_direction(head, path[0])

        if search_dir != Direction.NONE and (search_dir in dir_list):
            direction = search_dir
        else:
            direction = random.choice(ava_dirs)

        return direction

    # decides which direction

    def algo_decide_next(self):
        directions = ['up', 'left', 'down', 'right']
        print("================={}=================".format(self.turn))

        ava_dirs = self.ava_directions(directions)

        if ava_dirs:
            return self.fetch_nearest_food(ava_dirs)
        else:
            return random.choice(directions)

    def NN_decide_next(self, model):
        pass

    def ava_directions(self, all_directions):

        # check obstacle and return available direction

        my_snake = self.you
        head = my_snake.head()  # tuple (x,y)

        possible_dir = []
        if not self.board.is_obstacle((head[0], head[1] - 1)):
            possible_dir.append(Direction.UP)
        if not self.board.is_obstacle((head[0] - 1, head[1])):
            possible_dir.append(Direction.LEFT)
        if not self.board.is_obstacle((head[0], head[1] + 1)):
            possible_dir.append(Direction.DOWN)
        if not self.board.is_obstacle((head[0] + 1, head[1])):
            possible_dir.append(Direction.RIGHT)

        return possible_dir
