import pygame


DIRECTION_RIGHT = 4
DIRECTION_UP = 3
DIRECTION_LEFT = 2
DIRECTION_BOTTOM = 1

class Pacman:
    def __init__(self, x, y, w, h, speed, map_data, one_block_size):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.speed = speed
        self.direction = DIRECTION_RIGHT
        self.next_direction = DIRECTION_RIGHT
        self.map_data = map_data
        self.one_block_size = one_block_size
        self.score = 0  # локальный счёт

        # --- добавляем недостающие атрибуты для анимации ---
        self.frame_count = 7          # количество кадров анимации
        self.current_frame = 1        # текущий кадр
        self.last_anim_time = pygame.time.get_ticks()  # таймер для смены кадров

    def move_process(self):
        self.change_direction_if_possible()
        self.move_forwards()
        self.handle_teleport()
        if self.check_collisions():
            self.move_backwards()

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

    def change_direction_if_possible(self):
        if self.direction == self.next_direction: return
        temp = self.direction
        self.direction = self.next_direction
        self.move_forwards()
        if self.check_collisions():
            self.move_backwards()
            self.direction = temp
        else:
            self.move_backwards()

    def handle_teleport(self):
        map_width = len(self.map_data[0]) * self.one_block_size
        map_height = len(self.map_data) * self.one_block_size
        if self.x < 0: self.x = map_width - self.w
        elif self.x + self.w > map_width: self.x = 0
        if self.y < 0: self.y = map_height - self.h
        elif self.y + self.h > map_height: self.y = 0

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

    def eat(self, ghosts):
        i, j = self.get_map_y(), self.get_map_x()
        if self.map_data[i][j] == 2:
            self.map_data[i][j] = 3
            self.score += 1
        elif self.map_data[i][j] == 4:
            self.map_data[i][j] = 3
            self.score += 10
            for g in ghosts:
                g.make_vulnerable()

    def check_ghost_collision(self, ghosts):
        for ghost in ghosts:
            if ghost.get_map_x() == self.get_map_x() and ghost.get_map_y() == self.get_map_y():
                return True
        return False

    def get_map_x(self): return int(self.x / self.one_block_size)
    def get_map_y(self): return int(self.y / self.one_block_size)

    def draw(self, screen, pacman_frames):
        # обновляем анимацию каждые 100 мс
        now = pygame.time.get_ticks()
        if now - self.last_anim_time > 100:
            self.change_animation()
            self.last_anim_time = now

        # выбираем кадр анимации (базовый — рот вправо)
        frame_rect = pygame.Rect(
            (self.current_frame - 1) * self.one_block_size, 0,
            self.one_block_size, self.one_block_size
        )
        frame = pacman_frames.subsurface(frame_rect)

        # поворот/отражение по направлению движения
        if self.direction == DIRECTION_RIGHT:
            sprite = frame  # рот вправо — базовый кадр
        elif self.direction == DIRECTION_LEFT:
            sprite = pygame.transform.flip(frame, True, False)  # зеркалим по горизонтали
        elif self.direction == DIRECTION_UP:
            sprite = pygame.transform.rotate(frame, 90)  # вверх
        elif self.direction == DIRECTION_BOTTOM:
            sprite = pygame.transform.rotate(frame, -90)  # вниз
        else:
            sprite = frame

        screen.blit(sprite, (self.x, self.y))

    def change_animation(self):
        self.current_frame = 1 if self.current_frame == self.frame_count else self.current_frame + 1
