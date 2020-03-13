import json


class GameState:
    def __init__(self, turn, board, you):
        self.turn = turn
        self.board = board
        self.you = you

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)