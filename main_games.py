import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Змейка")

# Цвета
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Параметры игры
snake_size = 20
food_size = 15
stone_size = 20
snake_speed = 10
score = 0
best_score = 0

# Функция для отображения текущего счета
def draw_score():
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, BLACK)
    best_score_text = font.render(f"Best Score: {best_score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    screen.blit(best_score_text, (10, 40))

# Класс для змейки
class Snake:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.dx = snake_size
        self.dy = 0
        self.body = []

    def move(self):
        if len(self.body) > 0:
            self.body.pop()
            self.body.insert(0, (self.x, self.y))
        self.x += self.dx
        self.y += self.dy
        self.body.insert(0, (self.x, self.y))

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, RED, (segment[0], segment[1], snake_size, snake_size))

    def grow(self):
        self.body.append((self.x, self.y))

    def check_collision(self):
        if self.x < 0 or self.x >= screen_width or self.y < 0 or self.y >= screen_height:
            return True
        for segment in self.body[1:]:
            if self.x == segment[0] and self.y == segment[1]:
                return True
        return False

# Класс для еды
class Food:
    def __init__(self):
        self.x = random.randint(0, screen_width - food_size)
        self.y = random.randint(0, screen_height - food_size)
        self.rect = pygame.Rect(self.x, self.y, food_size, food_size)

    def draw(self):
        pygame.draw.rect(screen, GREEN, self.rect)

# Класс для камней
class Stone:
    def __init__(self):
        self.x = random.randint(0, screen_width - stone_size)
        self.y = random.randint(0, screen_height - stone_size)
        self.rect = pygame.Rect(self.x, self.y, stone_size, stone_size)

    def draw(self):
        pygame.draw.rect(screen, BLACK, self.rect)

# Создание объектов
snake = Snake()
food = Food()
stones = []

# Основной цикл игры
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        snake.dx = 0
        snake.dy = -snake_size
    elif keys[pygame.K_DOWN]:
        snake.dx = 0
        snake.dy = snake_size
    elif keys[pygame.K_LEFT]:
        snake.dx = -snake_size
        snake.dy = 0
    elif keys[pygame.K_RIGHT]:
        snake.dx = snake_size
        snake.dy = 0

    screen.fill(YELLOW)

    snake.move()
    snake.draw()
    food.draw()
    draw_score()

    if snake.check_collision():
        if score > best_score:
            best_score = score
        score = 0
        snake = Snake()
        food = Food()
        stones = []

    if snake.x == food.x and snake.y == food.y:
        score += 1
        snake.grow()
        food = Food()

    for stone in stones:
        stone.draw()

    pygame.display.flip()
    clock.tick(snake_speed)

pygame.quit()
sys.exit()
