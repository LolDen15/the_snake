from random import randint
from typing import Optional

import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет банана
BANANA_COLOR = (255, 255, 0)

# Цвет банана
ROCK_COLOR = (128, 128, 128)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 8

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Это базовый класс, от которого наследуются другие игровые объекты."""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        """Инициализация атрибутов родительского класса."""
        self.body_color = body_color
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def draw(self, surface):
        """
        Абстрактный метод, который предназначен
        для переопределения в дочерних классах.
        """
        pass


class Apple(GameObject):
    """Класс представляет яблоко, которое змейка может съесть."""

    def __init__(self, body_color=APPLE_COLOR):
        """Инициализация атрибутов класса Яблока."""
        super().__init__(body_color)
        self.randomize_position()
        self.position = self.randomize_position()

    @staticmethod
    def randomize_position():
        """Статический метод для получения случайной позиции объекта."""
        x: float = randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE
        y: float = randint(1, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE
        return x, y

    def draw(self, surface):
        """Метод для отрисовки объекта."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Banana(Apple):
    """Класс представляет банан, который змейка может съесть."""

    def __init__(self):
        """Инициализация атрибутов класса Банана."""
        super().__init__(body_color=BANANA_COLOR)


class Rock(Apple):
    """Класс представляет камень, на который змейка может наткнуться."""

    def __init__(self):
        """Инициализация атрибутов дочернего класса Камня."""
        super().__init__(body_color=ROCK_COLOR)


class Snake(GameObject):
    """Класс представляет змейку, которой управляет игрок."""

    def __init__(self):
        """Инициализация атрибутов класса Змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.length: int = 1
        self.last: Optional[tuple] = None
        self.next_direction: Optional[tuple] = None
        self.direction = RIGHT
        self.positions = [self.position]
        self.reset()

    def update_direction(self):
        """
        Метод для обновления направления
        после нажатия на направляющую кнопку.
        """
        if self.next_direction:
            self.direction: tuple = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для перемещения объекта по игровому полю."""
        current_head_position: tuple = self.get_head_position()
        dx, dy = self.direction
        new_head_position: tuple = (
            (current_head_position[0] + dx * GRID_SIZE) % SCREEN_WIDTH,
            (current_head_position[1] + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )

        if new_head_position in self.positions[2:]:
            self.reset()
        self.positions.insert(0, new_head_position)

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self, surface):
        """Метод для отрисовки объекта."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для получения позиции головы земейки."""
        return self.positions[0]

    def reset(self):
        """Метод для сброса змейки в начальное состояние."""
        self.length = 1
        if len(self.positions) > 1:
            del self.positions[1:]


def handle_keys(game_object):
    """Обработка нажатия клавиш."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция игры с бесконечным циклом."""
    apple = Apple()
    snake = Snake()
    banana = Banana()
    rock = Rock()
    while True:
        handle_keys(snake)
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        banana.draw(screen)
        rock.draw(screen)
        snake.draw(screen)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        if snake.get_head_position() == rock.position:
            rock.position = rock.randomize_position()
            snake.reset()
        if snake.get_head_position() == banana.position:
            banana.position = banana.randomize_position()
            if len(snake.positions) > 1:
                snake.length -= 1
                snake.last = snake.positions.pop()

        pygame.display.update()


if __name__ == '__main__':
    main()
