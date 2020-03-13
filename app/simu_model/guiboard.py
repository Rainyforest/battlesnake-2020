import random
import pygame

from basic_model.block import Block
from basic_model.occupant import Occupant
from simu_model.simuboard import SimuBoard
from simu_model.status import Status


class GuiBoard(SimuBoard):
    def __init__(self, height, width):
        super(GuiBoard, self).__init__(height,width)
        self.blocks = [[Block(Occupant.Empty) for w in range(self.width)] for h in range(self.height)]
        self.decided = False
        self.desired_directions = []
        self.desired_positions = []
        self.food_spawn_locations = []
        self.turn = 0

        self.color_set = {
            "Empty": (0, 0, 0),
            "SnakeBody": (200, 200, 0),
            "Food": (250, 20, 20),
            "Border": (255, 255, 255)
        }
        self.width_in_pixel = 500
        self.height_in_pixel = 500
        self.window = pygame.display.set_mode((self.width_in_pixel, self.height_in_pixel))  # Creates our screen object

    def draw_block(self, coord, color, eyes):
        dis = self.width_in_pixel // self.width  # Width/Height of each cube
        x, y = coord  # Current row
        pygame.draw.rect(self.window, color, (x * dis + 1, y * dis + 1, dis - 2, dis - 2))

        if eyes:  # Draws the eyes
            centre = dis // 2
            radius = 3
            circle_middle = (x * dis + centre - radius, y * dis + 8)
            circle_middle2 = (x * dis + dis - radius * 2, y * dis + 8)
            pygame.draw.circle(self.window, self.color_set["Empty"], circle_middle, radius)
            pygame.draw.circle(self.window, self.color_set["Empty"], circle_middle2, radius)

    def draw_grid(self):
        w = self.height_in_pixel
        size_btwn = w // self.height  # Gives us the distance between the lines

        x = 0  # Keeps track of the current x
        y = 0  # Keeps track of the current y
        for l in range(self.height):  # We will draw one vertical and one horizontal line each loop
            x = x + size_btwn
            y = y + size_btwn
            pygame.draw.line(self.window, self.color_set["Border"], (x, 0), (x, w))
            pygame.draw.line(self.window, self.color_set["Border"], (0, y), (w, y))

    def redraw_window(self):
        # random.randint(0,255), random.randint(0,255), random.randint(0,255)
        self.window.fill(self.color_set["Empty"])  # Fills the screen with black
        #
        for snake in self.snake_list:
            if snake.status != Status.Alive:
                continue
            body_list = snake.body_list
            snake_color = (random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self.draw_block(body_list[0],snake_color,True)
            for body in body_list[1:]:
                self.draw_block(body,snake_color,False)
                #
        for food in self.food_list:
            self.draw_block(food,self.color_set["Food"],False)
        self.draw_grid()  # Will draw our grid lines
        pygame.display.update()  # Updates the screen

    def message_box(self, subject, content):
        pass

    def render(self):
        clock = pygame.time.Clock()  # creating a clock object
        flag = True
        self.redraw_window()

