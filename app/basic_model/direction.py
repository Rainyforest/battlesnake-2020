import random
from enum import Enum


class Direction(Enum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3
    NONE = -1
    @staticmethod
    def opposite(d):
        """Return the opposite direction."""
        if d == Direction.LEFT:
            return Direction.RIGHT
        elif d == Direction.RIGHT:
            return Direction.LEFT
        elif d == Direction.UP:
            return Direction.DOWN
        elif d == Direction.DOWN:
            return Direction.UP
        else:
            return Direction.NONE

    def __str__(self):
        if self == Direction.LEFT: return "LEFT"
        elif self == Direction.RIGHT: return "RIGHT"
        elif self == Direction.UP: return "UP"
        elif self == Direction.DOWN: return "DOWN"
        else : return "NONE"
