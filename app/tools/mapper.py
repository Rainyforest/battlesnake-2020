from basic_model.board import Board
from basic_model.gamestate import GameState
from basic_model.occupant import Occupant
from basic_model.snake import Snake
from simu_model.guiboard import GuiBoard
from simu_model.simuboard import SimuBoard
from simu_model.simusnake import SimuSnake


def apigamestate_to_simu(gamestate) -> GuiBoard:
    apiboard = gamestate.board
    simuboard = GuiBoard(apiboard.height, apiboard.width)
    simuboard.turn = gamestate.turn

    # Place all food on the board
    for f in apiboard.food_list:
        if simuboard.blocks[f[1]][f[0]].occupant != Occupant.Empty:
            print("Fail to place food on occupied tile, all fruits are {}".format(apiboard.food_list))
            continue

        simuboard.blocks[f[1]][f[0]].place(Occupant.Food)
        added = simuboard.food_list.append(f)
        # assert added

    # Traverse through all snakes
    for i in range(len(apiboard.snake_list)):
        s = apiboard.snake_list[i]
        # map snake to simusnake world
        simusnake = SimuSnake(i, s.head(), simuboard)
        ## Set meta data
        simusnake.health = s.health
        simusnake.body_list = s.body_list
        simusnake.head = s.head()
        simusnake.tail = s.tail()
        simusnake.max_len = s.length()
        simusnake.pending_max_len = s.length()
        simusnake.length = s.effective_length
        simuboard.snake_list.append(simusnake)
        return simuboard


def simu_to_gamestate(simuboard : SimuBoard, id) -> GameState:
    gamestate = GameState(simuboard.turn, simuboard, simuboard.snake_list[id])
    return gamestate
