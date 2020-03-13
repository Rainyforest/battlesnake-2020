from basic_model.occupant import Occupant
from basic_model.snake import Snake
from simu_model.status import Status
from tools.utils import *


class SimuSnake(Snake):
    def __init__(self, id, init_head_pos, world):
        self.id = id
        self.health = self.SNAKE_MAX_HEALTH
        self.body_list = [init_head_pos] * 3
        self.max_len = 3
        self.pending_max_len = self.max_len
        self.length = 3
        self.status = Status.Alive
        self.world = world

    SNAKE_MAX_HEALTH = 100

    def alive(self):
        return self.status == Status.Alive

    def starve(self):
        self.health = self.health - 1

    def grow(self):
        self.pending_max_len = self.pending_max_len + 1
        if self.pending_max_len > self.max_len:
            self.length = self.length + 1
        self.health = 101  # +1 because health decreases every term

    def peek_length(self):
        if self.length == self.max_len:
            return self.length
        else:
            return self.length + 1

    def update_post_tick(self):
        self.max_len = self.pending_max_len

    def kill(self, kill_reason):
        if kill_reason == Status.Alive: print("Error, wrong kill reason.")
        self.health = 0
        for body in self.body_list:
            self.world.blocks[body[1]][body[0]].empty()
        self.body_list = []
        self.status = kill_reason

    def will_grow_on_update(self):
        return self.length != self.max_len

    def move_tail(self):

        curr_tail = self.tail()
        tail_block = self.world.blocks[curr_tail[1]][curr_tail[0]]
        if self.max_len != self.pending_max_len - 1 :
            tail_block.empty()
            self.body_list = self.body_list[:-1]
        self.length = self.length - 1

    def move_head(self, d):
        curr_head = self.head()
        new_head = advance(curr_head, d)
        self.body_list.insert(0,new_head)
        new_block = self.world.blocks[new_head[1]][new_head[0]]
        new_block.place(Occupant.SnakeBody)
        new_block.set_id(self.id)
        self.length = self.length + 1
