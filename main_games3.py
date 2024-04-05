import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")

# Цвета
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BROWN = (165, 42, 42)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Параметры игры
block_size = 20
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 40)


# Класс змейки
class Snake:
    def __init__(self):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.length = 3
        self.body = [[self.x, self.y]]
        self.direction = 'RIGHT'

    def move(self):
        if self.direction == 'UP':
            self.y -= block_size
        elif self.direction == 'DOWN':
            self.y += block_size
        elif self.direction == 'LEFT':
            self.x -= block_size
        elif self.direction == 'RIGHT':
            self.x += block_size

        self.body.insert(0, [self.x, self.y])
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, RED, pygame.Rect(segment[0], segment[1], block_size, block_size))

    def grow(self):
        self.length += 1

    def collide(self):
        if self.x < 0:
            self.x = screen_width
        elif self.x >= screen_width:
            self.x = 0
        elif self.y < 0:
            self.y = screen_height
        elif self.y >= screen_height:
            self.y = 0


# Класс еды
class Food:
    def __init__(self):
        self.x = random.randrange(0, screen_width, block_size)
        self.y = random.randrange(0, screen_height, block_size)

    def draw(self):
        pygame.draw.rect(screen, GREEN, pygame.Rect(self.x, self.y, block_size, block_size))


# Класс камней
class Stone:
    def __init__(self):
        self.x = random.randrange(0, screen_width, block_size)
        self.y = 0 - block_size

    def draw(self):
        pygame.draw.rect(screen, BROWN, pygame.Rect(self.x, self.y, block_size, block_size))

    def move(self):
        self.y += block_size

    @staticmethod
    def spawn_stones(stones):
        if random.randint(0, 100) < 2:  # Вероятность появления камня
            x = random.randrange(0, screen_width - block_size, block_size)
            y = -block_size  # Камень появляется сверху экрана
            stone = Stone()
            stone.x = x
            stone.y = y
            stones.append(stone)


# Класс стенок
class Wall:
    def __init__(self):
        self.walls = []
        for _ in range(5):
            wall_x = random.randrange(0, screen_width, block_size)
            wall_y = random.randrange(0, screen_height, block_size)
            self.walls.append([wall_x, wall_y])

    def draw(self):
        for wall in self.walls:
            pygame.draw.rect(screen, BLACK, pygame.Rect(wall[0], wall[1], block_size, block_size))


# Функция вывода текста на экран
def draw_text(text, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


# Функция обработки событий
def event_handler(snake):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and snake.direction != 'DOWN':
                snake.direction = 'UP'
            elif event.key == pygame.K_DOWN and snake.direction != 'UP':
                snake.direction = 'DOWN'
            elif event.key == pygame.K_LEFT and snake.direction != 'RIGHT':
                snake.direction = 'LEFT'
            elif event.key == pygame.K_RIGHT and snake.direction != 'LEFT':
                snake.direction = 'RIGHT'


# Игровой цикл
def main():
    snake = Snake()
    food = Food()
    stones = []
    walls = Wall()
    score = 0
    speed = 3

    stone_spawn_time = 0
    food_spawn_time = 0

    while True:
        event_handler(snake)
        screen.fill(YELLOW)

        current_time = pygame.time.get_ticks()

        if current_time - stone_spawn_time > 50000:
            Stone.spawn_stones(stones)
            stone_spawn_time = current_time

        if current_time - food_spawn_time > 40000:
            food = Food()
            food_spawn_time = current_time

        snake.move()
        snake.collide()
        snake.draw()

        food.draw()

        for stone in stones:
            stone.draw()
            stone.move()
            if snake.body[0] == [stone.x, stone.y]:
                snake.length -= 2
                stones.remove(stone)

        for wall in walls.walls:
            pygame.draw.rect(screen, BLACK, pygame.Rect(wall[0], wall[1], block_size, block_size))
            if snake.body[0] == wall:
                snake.length -= 4

        if snake.body[0] == [food.x, food.y]:
            snake.grow()
            food = Food()
            score += 1

        draw_text(f'Score: {score}', BLACK, 10, 10)

        pygame.display.flip()
        clock.tick(speed)


if __name__ == "__main__":
    main()
