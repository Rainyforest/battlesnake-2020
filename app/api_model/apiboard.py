from api_model.apisnake import APISnake
from basic_model.board import Board


class APIBoard(Board):
    def __init__(self, board_data):
        self.height = board_data['height']
        self.width = board_data['width']
        self.food_list = self.food_list(board_data['food'])
        self.snake_list = self.snake_list(board_data['snakes'])

    def my_snake(self):
        return self.snake_list[0]

    @staticmethod
    def snake_list(snake_data):
        snake_list = []
        for snake in snake_data:
            new_snake = APISnake(snake)
            snake_list.append(new_snake)
        return snake_list

    @staticmethod
    def food_list(food_data):
        food_list = []
        for food_dic in food_data:
            x = food_dic["x"]
            y = food_dic["y"]
            food_list.append((x, y))
        return food_list

