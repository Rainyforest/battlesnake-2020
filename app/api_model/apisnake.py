from basic_model.snake import Snake


class APISnake(Snake):
    def __init__(self, snake_data):
        self.id = snake_data['id']
        self.name = snake_data['name']
        self.health = snake_data['health']
        self.body_list = self.body_list(snake_data['body'])
        self.effective_length = self.effective_length()
        self.growth_left = self.growth_left()

    @staticmethod
    def body_list(body_dic_list):
        body_list = []
        for body_dic in body_dic_list:
            x = body_dic["x"]
            y = body_dic["y"]
            body_list.append((x, y))
        return body_list

    def effective_length(self):
        return self.length() - self.growth_left()

    def growth_left(self):
        # API stores duplicate body parts at end of snake if growing,
        # thus can determine growth left

        result = 0
        for i in range(self.length() - 2, -1, -1):
            if self.body_list[i] == self.tail():
                result = result + 1
            else:
                break
        return result