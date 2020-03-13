from api_model.apiboard import APIBoard
from api_model.apisnake import APISnake
from basic_model.gamestate import GameState


class APIGameState(GameState):
    def __init__(self, data):
        self.game = data['game']
        self.turn = data['turn']
        self.board = APIBoard(data['board'])
        self.you = APISnake(data['you'])








