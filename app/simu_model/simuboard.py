import random

from basic_model.block import Block
from basic_model.board import Board
from basic_model.occupant import Occupant
from simu_model.simusnake import SimuSnake
from simu_model.status import Status
from tools.utils import advance


class SimuBoard(Board):
    def __init__(self, height, width):
        super(SimuBoard, self).__init__(height, width)  # inherit height, width, food_list, snake_list
        self.blocks = [[Block(Occupant.Empty) for w in range(self.width)] for h in range(self.height)]
        self.decided = False
        self.desired_directions = []
        self.desired_positions = []
        self.food_spawn_locations = []
        self.turn = 0

    FOOD_SPAWN_CHANCE = 0.15
    SNAKE_MAX_HEALTH = 100
    SNAKE_START_SIZE = 3

    def __str__(self):
        str_mat = ""
        for row in self.blocks:
            for block in row:
                content = ''
                if block.occupant == Occupant.Empty:
                    content = '-'
                elif block.occupant == Occupant.Food:
                    content = 'x'
                elif block.occupant == Occupant.SnakeBody:
                    content = str(block.id)
                str_mat = str_mat + content + " "
            str_mat = str_mat + "\n"
        return str_mat

    def init_snakes(self, number_of_snakes):
        mn, md, mx = 1, (self.width - 1) // 2, self.width - 2

        start_positions = [
            (mn, mn),
            (mn, md),
            (mn, mx),
            (md, mn),
            (md, mx),
            (mx, mn),
            (mx, md),
            (mx, mx)
        ]

        # randomly order positions
        random.shuffle(start_positions)

        for i in range(number_of_snakes):
            snake_body_list = [start_positions[i]] * self.SNAKE_START_SIZE
            snake = SimuSnake(i, start_positions[i], self)
            self.snake_list.append(snake)

    def init_food(self, number_of_snakes):
        empty_block_list = self.get_empty_block_list()
        locations = random.choices(empty_block_list, k=number_of_snakes)
        for location in locations:
            self.food_list.append(location)
            self.blocks[location[1]][location[0]].place(Occupant.Food)

    def is_decided(self):
        alive_num = 0
        for snake in self.snake_list:
            if snake.status == Status.Alive:
                alive_num = alive_num + 1

        return alive_num < 1

    def hit_wall(self, coord):
        x, y = coord
        return x < 0 or y < 0 or x >= self.width or y >= self.height

    # KilledWall Check
    def update_killed_wall(self):
        for i in range(len(self.snake_list)):
            if not self.snake_list[i].alive():
                continue
            pos = self.desired_positions[i]
            if self.hit_wall(pos):
                self.snake_list[i].kill(Status.KilledWall)

    # KilledHeadOnHead Check
    def update_killed_head_on_head(self):
        for i in range(len(self.snake_list)):
            if not self.snake_list[i].alive():
                continue
            target = self.desired_positions[i]
            matches = 1
            # What's the longest tail
            longest = self.snake_list[i].peek_length()
            # Count how  many snake_list have length matching longest
            longest_count = 1
            for j in range(i + 1, len(self.snake_list)):
                if not self.snake_list[j].alive():
                    continue
                if self.desired_positions[j] == target:
                    matches = matches + 1

                    # longest excelled, reset longest counter
                    if longest < self.snake_list[j].peek_length():
                        longest = self.snake_list[j].peek_length()
                        longest_count = 1
                    # longest matched increase longest counter
                    elif longest == self.snake_list[j].peek_length():
                        longest_count = longest_count + 1

            # if no collision, skip
            if matches == 1:
                continue

            # kill all that would be killed by multi-way collision
            for j in range(i, len(self.snake_list)):
                if not self.snake_list[i].alive():
                    continue
                # kill if shorter than longest or if more than 1 longest
                if self.desired_positions[j] == target and (self.snake_list[j].peek_length() or longest_count > 1):
                    self.snake_list[j].kill(Status.KilledHeadOnHead)

    def update_eat_food(self):
        for i in range(len(self.snake_list)):
            if not self.snake_list[i].alive():
                continue

            new_head = self.desired_positions[i]

            if self.blocks[new_head[1]][new_head[0]].occupant == Occupant.Food:
                self.food_list.remove(new_head)  # eat food
                self.blocks[new_head[1]][new_head[0]].empty()
                self.snake_list[i].grow()

    def update_killed_head_on_body(self):
        for i in range(len(self.snake_list)):
            if not self.snake_list[i].alive():
                continue

            new_head = self.desired_positions[i]

            block = self.blocks[new_head[1]][new_head[0]]
            if block.occupant == Occupant.SnakeBody:
                # If colliding into the end of another snake, need to check
                # whether the other snake will grow, in which case this kills
                # the current snake, or if the other snake will not grow, freeing
                # the tile simultaneously
                if (not self.snake_list[block.id].tail == new_head or self.snake_list[block.id].will_grow_on_update) and self.turn >= 2:
                    if block.id == i:
                        self.snake_list[i].kill(Status.KilledOwnBody)
                    else:
                        self.snake_list[i].kill(Status.KilledEnemyBody)

    def update_killed_starvation(self):
        for i in range(len(self.snake_list)):
            if not self.snake_list[i].alive():
                continue
            self.snake_list[i].starve()
            if self.snake_list[i].health <= 0:
                self.snake_list[i].kill(Status.KilledStarvation)

    def update_desired_positions(self):
        if len(self.desired_directions) != len(self.snake_list):
            print("Error, Dimension not agree.")
        self.desired_positions = []  # desired new position
        for i in range(len(self.snake_list)):
            s = self.snake_list[i]
            if s.alive():
                self.desired_positions.append(advance(s.head(), self.desired_directions[i]))
            else:
                self.desired_positions.append((-1, -1))  # add an invalid position

    def update_movement(self):
        for i in range(len(self.snake_list)):
            if self.snake_list[i].alive():
                self.snake_list[i].move_tail()
        for i in range(len(self.snake_list)):
            if self.snake_list[i].alive():
                self.snake_list[i].move_head(self.desired_directions[i])

    def update_length(self):
        for s in self.snake_list:
            s.update_post_tick()

    def update_turn(self):
        self.turn = self.turn + 1

    def update_decided(self):
        self.decided = self.is_decided()

    def step(self):
        self.update_desired_positions()
        self.update_killed_wall()
        self.update_killed_starvation()
        self.update_killed_head_on_head()
        self.update_eat_food()
        self.update_killed_head_on_body()
        self.update_movement()
        self.update_length()
        self.update_spawn_food()
        self.update_decided()
        self.update_turn()



    def update_spawn_food(self):

        if random.random() < self.FOOD_SPAWN_CHANCE:
            if len(self.food_spawn_locations) > 0:
                locations = [self.food_spawn_locations[0]]
                self.food_spawn_locations = self.food_spawn_locations[1:]
            else:
                ebl = self.get_empty_block_list()
                if ebl:
                    locations = random.choices(ebl, k=1)
                    for location in locations:
                        self.food_list.append(location)
                        self.blocks[location[1]][location[0]].place(Occupant.Food)

    def get_empty_block_list(self):
        ebl = []
        for y in range(self.height):
            for x in range(self.width):
                if self.blocks[y][x].occupant == Occupant.Empty:
                    ebl.append((x, y))
        return ebl

