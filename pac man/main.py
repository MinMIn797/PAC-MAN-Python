import pygame, sys
from pacman import Pacman, DIRECTION_LEFT, DIRECTION_RIGHT, DIRECTION_UP, DIRECTION_BOTTOM
from ghost import Ghost
from map_data import map_data

# --- Константы ---
lives = 3
fps = 30
one_block_size = 20

# --- Инициализация pygame ---
pygame.init()
screen_width = len(map_data[0]) * one_block_size
screen_height = len(map_data) * one_block_size + 40
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 20)

# --- Загрузка спрайтов ---
pacman_frames = pygame.image.load("assets/animations (1).gif").convert_alpha()
ghost_images = [
    pygame.image.load("assets/red.png").convert_alpha(),
    pygame.image.load("assets/orange.png").convert_alpha(),
    pygame.image.load("assets/green.png").convert_alpha(),
    pygame.image.load("assets/blue.png").convert_alpha(),
]

# --- Инициализация объектов ---
pacman = Pacman(one_block_size, one_block_size, one_block_size, one_block_size,
                one_block_size//5, map_data, one_block_size)

ghosts = [
    Ghost(9*one_block_size, 10*one_block_size, one_block_size, one_block_size,
          pacman.speed//2, pacman, map_data, one_block_size, ghost_images[i])
    for i in range(4)
]

# --- Вспомогательные функции ---
def create_rect(x, y, w, h, color):
    pygame.draw.rect(screen, color, (x, y, w, h))

def draw_foods():
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] == 2:
                create_rect(j*one_block_size+one_block_size//3, i*one_block_size+one_block_size//3,
                            one_block_size//3, one_block_size//3, (254,184,151))

def draw_walls():
    for i in range(len(map_data)):
        for j in range(len(map_data[0])):
            if map_data[i][j] == 1:
                create_rect(j*one_block_size, i*one_block_size, one_block_size, one_block_size, (52,45,202))

def draw_score():
    text = font.render(f"Score: {pacman.score}", True, (255,255,255))
    screen.blit(text, (0, screen_height - 30))

def draw_lives():
    text = font.render(f"Lives: {lives}", True, (255,255,255))
    screen.blit(text, (220, screen_height - 30))

def draw_ghosts():
    for g in ghosts:
        g.draw(screen)

def update_ghosts():
    for g in ghosts:
        g.move_process()

def restart_pacman_and_ghosts():
    global pacman, ghosts
    # создаём нового Pacman
    pacman = Pacman(
        one_block_size, one_block_size,
        one_block_size, one_block_size,
        one_block_size//5, map_data, one_block_size
    )
    # создаём новых призраков (каждый со своей картинкой)
    ghosts = [
        Ghost(9*one_block_size, 10*one_block_size, one_block_size, one_block_size,
              pacman.speed//2, pacman, map_data, one_block_size, ghost_images[0]),
        Ghost(9*one_block_size, 10*one_block_size, one_block_size, one_block_size,
              pacman.speed//2, pacman, map_data, one_block_size, ghost_images[1]),
        Ghost(9*one_block_size, 10*one_block_size, one_block_size, one_block_size,
              pacman.speed//2, pacman, map_data, one_block_size, ghost_images[2]),
        Ghost(9*one_block_size, 10*one_block_size, one_block_size, one_block_size,
              pacman.speed//2, pacman, map_data, one_block_size, ghost_images[3]),
    ]



def game_over():
    global lives
    text = font.render("GAME OVER", True, (255, 0, 0))
    # выводим сообщение в центр экрана
    screen.blit(text, (screen_width // 2 - text.get_width() // 2,
                       screen_height // 2 - text.get_height() // 2))
    pygame.display.flip()
    # ждём 3 секунды
    pygame.time.wait(3000)
    # сбрасываем жизни и перезапускаем игру
    lives = 3
    restart_pacman_and_ghosts()


# --- Игровой цикл ---
def game_loop():
    global lives
    running = True
    while running:
        screen.fill((0,0,0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a): pacman.next_direction = DIRECTION_LEFT
                elif event.key in (pygame.K_RIGHT, pygame.K_d): pacman.next_direction = DIRECTION_RIGHT
                elif event.key in (pygame.K_UP, pygame.K_w): pacman.next_direction = DIRECTION_UP
                elif event.key in (pygame.K_DOWN, pygame.K_s): pacman.next_direction = DIRECTION_BOTTOM

        pacman.move_process()
        pacman.eat()
        update_ghosts()

        if pacman.check_ghost_collision(ghosts):
            lives -= 1
            restart_pacman_and_ghosts()
            if lives == 0:
                game_over()

        draw_walls()
        draw_foods()
        pacman.draw(screen, pacman_frames)
        draw_ghosts()
        draw_score()
        draw_lives()

        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    game_loop()
