import sys 
import pygame
import random
import copy
import os
from astar import Position, Map

# Create grid 
# Create empty list
class Ultilities:
    @staticmethod
    def init_pygame():
        os.environ["SDL_VIDEO_WINDOW_POS"] = "50,50"
        pygame.init()

    @staticmethod
    def create_grid(row_num, col_num):
        grid = []
        for row in range(0, row_num):
            a_row = []
            for col in range(0, col_num):
                a_row.append(0)
            grid.append(a_row)
        return grid

class Grid:
    NO_WALL_ID = 0
    WALL_ID = 1
    PLAYER_ID = 2
    START_END_ID = 3

    def __init__(self, row_num=10, col_num=10):
        self.grid = Ultilities.create_grid(row_num, col_num)
        self.row_num = row_num 
        self.col_num = col_num
        self.rect_size = [20, 20]
        self.margin = 5
        self.map = None

    def load_map(self, map):
        self.map = map
        self.row_num = map.size
        self.col_num = map.size 
        self.grid = copy.deepcopy(map.map)
    
    def calculate_rect_size(self, screen_width, screen_height):
        self.rect_size[0] = (screen_width - self.margin * (self.col_num + 1)) / self.col_num
        self.rect_size[1] = (screen_height - self.margin * (self.row_num + 1)) / self.row_num

    def randomize(self):
        for row in range(self.row_num):
            for col in range(self.col_num):
                self.grid[row][col] = random.randint(0, 1)

    def set_grid_item(self, x, y, value):
        self.grid[x][y] = value
    
    def get_grid_item(self, x, y):
        return self.grid[x][y]

    def is_valid_position(self, x, y):
        if self.map:
            return self.map.is_valid(x, y) and not self.map.is_wall(x, y)
        return x >= 0 and x < self.row_num and y >= 0 and y < self.col_num 

class Color:
    COLOR_DICT = dict(
        BLACK = (0, 0, 0),
        WHITE = (255, 255, 255),
        GREEN = (0, 255, 0),
        RED = (255, 0, 0),
        BLUE = (0, 0, 255)
    )

class Window:
    def __init__(self, width=800, height=600, title="Pygame Application"):
        self.size = [width, height]
        self.title = title
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(title)

    def display(self):
        pygame.display.flip()

class Application:
    def __init__(self):
        self.window = Window()
        self.is_done = False
        self.clock = pygame.time.Clock()
        # Set key repeat interval
        pygame.key.set_repeat(100, 100)

        self.player_position = Position()
        self.direction_key = [pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT]
        self.start = dict( position = Position(-1, -1), added = False )
        self.end = dict( position = Position(-1, -1), added = False )

        self.grid = Grid(20, 20)
        self.grid.calculate_rect_size(self.window.size[0], self.window.size[1])
        self.grid.set_grid_item(0, 0, Grid.PLAYER_ID)

    def load_map(self, map):
        self.grid.load_map(map)
        self.grid.calculate_rect_size(self.window.size[0], self.window.size[1])

        self.start = dict( position = Position(-1, -1), added = False )
        self.end = dict( position = Position(-1, -1), added = False )

        for row in range(self.grid.row_num):
            for col in range(self.grid.col_num):
                if self.grid.get_grid_item(row, col) == Grid.NO_WALL_ID:
                    self.player_position = Position(row, col)
                    self.grid.set_grid_item(row, col, Grid.PLAYER_ID)
                    return

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_done = True
                elif event.key in self.direction_key:
                    self.handle_player_movement(event)
                elif event.key == pygame.K_SPACE:
                    self.choose_start_end()

    def handle_player_movement(self, event):
        new_pos = Position(self.player_position.x, self.player_position.y)
        if event.key == pygame.K_UP:
            new_pos.x = self.player_position.x - 1
        elif event.key == pygame.K_DOWN:
            new_pos.x = self.player_position.x + 1
        elif event.key == pygame.K_RIGHT:
            new_pos.y = self.player_position.y + 1
        elif event.key == pygame.K_LEFT:
            new_pos.y = self.player_position.y - 1
        
        if self.grid.is_valid_position(new_pos.x, new_pos.y):
            # Clear old position
            if self.player_position != self.start["position"] and self.player_position != self.end["position"]:
                self.grid.set_grid_item(self.player_position.x, self.player_position.y, Grid.NO_WALL_ID)
            self.player_position = new_pos
            self.grid.set_grid_item(self.player_position.x, self.player_position.y, Grid.PLAYER_ID)
    
    def choose_start_end(self):
        if not self.start["added"]:
            self.start["position"] = copy.deepcopy(self.player_position)
            self.start["added"] = True
            self.grid.set_grid_item(self.start["position"].x, self.start["position"].y, Grid.START_END_ID)
        elif not self.end["added"]:
            self.end["position"] = copy.deepcopy(self.player_position)
            self.end["added"] = True
            self.grid.set_grid_item(self.end["position"].x, self.end["position"].y, Grid.START_END_ID)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LCTRL] and keys[pygame.K_l]:
            self.clear()
    
    def clear(self):
        if self.start["added"]:
            self.grid.set_grid_item(self.start["position"].x, self.start["position"].y, Grid.NO_WALL_ID)
            self.start["position"] = Position(-1, -1)
            self.start["added"] = False
        if self.end["added"]:
            self.grid.set_grid_item(self.end["position"].x, self.end["position"].y, Grid.NO_WALL_ID)
            self.end["position"] = Position(-1, -1)
            self.end["added"] = False

    def update(self):
        pass
    
    def render(self):
        self.window.screen.fill(Color.COLOR_DICT["BLACK"])
        for row in range(self.grid.row_num):
            for col in range(self.grid.col_num):
                color = Color.COLOR_DICT["WHITE"]
                if self.grid.grid[row][col] == Grid.PLAYER_ID:
                    color = Color.COLOR_DICT["GREEN"]
                elif self.grid.grid[row][col] == Grid.START_END_ID:
                    color = Color.COLOR_DICT["RED"]
                elif self.grid.grid[row][col] == Grid.WALL_ID:
                    color = Color.COLOR_DICT["BLUE"]

                pygame.draw.rect(self.window.screen, color, [
                    (self.grid.rect_size[0] + self.grid.margin) * col + self.grid.margin,
                    (self.grid.rect_size[1] + self.grid.margin) * row + self.grid.margin,
                    self.grid.rect_size[0],
                    self.grid.rect_size[1]
                ])
        self.window.display()

    def run(self):
        while not self.is_done:
            self.handle_event()
            self.handle_input()
            self.update()
            self.render()
            self.clock.tick(60)
        pygame.quit()

if __name__ == "__main__":
    Ultilities.init_pygame()
    app = Application()
    map = Map()
    map.read_from_file("input.txt")
    app.load_map(map)
    app.run()