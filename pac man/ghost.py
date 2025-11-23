import pygame
import math
import random

DIRECTION_RIGHT = 4
DIRECTION_UP = 3
DIRECTION_LEFT = 2
DIRECTION_BOTTOM = 1

class Ghost:
    def __init__(self, x, y, width, height, speed, pacman, map_data, one_block_size, image):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.speed = speed
        self.direction = DIRECTION_RIGHT
        self.pacman = pacman
        self.map_data = map_data
        self.one_block_size = one_block_size
        self.range = 6
        self.image = pygame.transform.scale(image, (one_block_size, one_block_size))

        self.random_targets = [
            {"x": 1 * one_block_size, "y": 1 * one_block_size},
            {"x": 1 * one_block_size, "y": (len(map_data) - 2) * one_block_size},
            {"x": (len(map_data[0]) - 2) * one_block_size, "y": one_block_size},
            {"x": (len(map_data[0]) - 2) * one_block_size, "y": (len(map_data) - 2) * one_block_size},
        ]
        self.randomTargetIndex = random.randint(0, 3)
        self.target = self.random_targets[self.randomTargetIndex]

    def get_map_x(self): return int(self.x / self.one_block_size)
    def get_map_y(self): return int(self.y / self.one_block_size)

    def is_in_range(self):
        dx = abs(self.pacman.get_map_x() - self.get_map_x())
        dy = abs(self.pacman.get_map_y() - self.get_map_y())
        return math.sqrt(dx**2 + dy**2) <= self.range

    def move_process(self):
        if self.is_in_range():
            self.target = self.pacman
        else:
            self.target = self.random_targets[self.randomTargetIndex]

        self.change_direction_if_possible()
        self.move_forwards()
        if self.check_collisions():
            self.move_backwards()
            self.randomTargetIndex = random.randint(0, 3)

    def move_forwards(self):
        if self.direction == DIRECTION_RIGHT: self.x += self.speed
        elif self.direction == DIRECTION_LEFT: self.x -= self.speed
        elif self.direction == DIRECTION_UP: self.y -= self.speed
        elif self.direction == DIRECTION_BOTTOM: self.y += self.speed

    def move_backwards(self):
        if self.direction == DIRECTION_RIGHT: self.x -= self.speed
        elif self.direction == DIRECTION_LEFT: self.x += self.speed
        elif self.direction == DIRECTION_UP: self.y += self.speed
        elif self.direction == DIRECTION_BOTTOM: self.y -= self.speed

    def check_collisions(self):
        m = self.map_data
        bs = self.one_block_size
        rows, cols = len(m), len(m[0])
        cells = [
            (int(self.y / bs), int(self.x / bs)),
            (int(self.y / bs + 0.9999), int(self.x / bs)),
            (int(self.y / bs), int(self.x / bs + 0.9999)),
            (int(self.y / bs + 0.9999), int(self.x / bs + 0.9999)),
        ]
        for cy, cx in cells:
            if cy < 0 or cy >= rows or cx < 0 or cx >= cols: return True
            if m[cy][cx] == 1: return True
        return False

    def change_direction_if_possible(self):
        temp_dir = self.direction
        destX = self.target.get_map_x() if hasattr(self.target, "get_map_x") else int(self.target["x"] / self.one_block_size)
        destY = self.target.get_map_y() if hasattr(self.target, "get_map_y") else int(self.target["y"] / self.one_block_size)
        new_dir = self.calculate_new_direction(self.map_data, destX, destY)
        if new_dir is None: return
        self.direction = new_dir
        self.move_forwards()
        if self.check_collisions():
            self.move_backwards()
            self.direction = temp_dir
        else:
            self.move_backwards()

    def calculate_new_direction(self, map_data, destX, destY):
        rows, cols = len(map_data), len(map_data[0])
        startX, startY = self.get_map_x(), self.get_map_y()
        queue = [{"x": startX, "y": startY, "moves": []}]
        visited = [[False] * cols for _ in range(rows)]

        while queue:
            node = queue.pop(0)
            x, y, moves = node["x"], node["y"], node["moves"]
            if visited[y][x]: continue
            visited[y][x] = True
            if x == destX and y == destY:
                return moves[0] if moves else None
            for nx, ny, dir_ in self.add_neighbors(x, y, map_data):
                if not visited[ny][nx] and map_data[ny][nx] != 1:
                    queue.append({"x": nx, "y": ny, "moves": moves + [dir_]})
        return None

    def add_neighbors(self, x, y, mp):
        rows, cols = len(mp), len(mp[0])
        neighbors = []
        if x > 0 and mp[y][x - 1] != 1: neighbors.append((x - 1, y, DIRECTION_LEFT))
        if x < cols - 1 and mp[y][x + 1] != 1: neighbors.append((x + 1, y, DIRECTION_RIGHT))
        if y > 0 and mp[y - 1][x] != 1: neighbors.append((x, y - 1, DIRECTION_UP))
        if y < rows - 1 and mp[y + 1][x] != 1: neighbors.append((x, y + 1, DIRECTION_BOTTOM))
        return neighbors

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
