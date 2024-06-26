from random import randint
from typing import Optional

import pygame as pg

# Инициализация PyGame:
pg.init()

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

CONTROL_DICT = {
    (LEFT, pg.K_UP): UP,
    (RIGHT, pg.K_UP): UP,
    (LEFT, pg.K_DOWN): DOWN,
    (RIGHT, pg.K_DOWN): DOWN,
    (UP, pg.K_LEFT): LEFT,
    (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT,
    (DOWN, pg.K_RIGHT): RIGHT
}

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
SPEED = 12

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


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
        raise NotImplementedError(
            'Это абстрактный метод для переопределения в дочерних классах'
        )

    def generate_rect(self, surface, position, color):
        """Метод для получения размера одной ячейки"""
        rect = pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, color, rect)
        if color != BOARD_BACKGROUND_COLOR:
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Food(GameObject):
    """Класс представляет еду, которую змейка может съесть."""

    def __init__(self, positions=None, body_color=APPLE_COLOR):
        """Инициализация атрибутов класса Яблока."""
        super().__init__(body_color)
        self.randomize_position(positions)

    def randomize_position(self, positions):
        """Метод для получения случайной позиции объекта."""
        while True:
            if positions and self.position in positions:
                xy = (randint(0, SCREEN_WIDTH // GRID_SIZE - 1) * GRID_SIZE,
                      randint(1, SCREEN_HEIGHT // GRID_SIZE - 1) * GRID_SIZE)
                self.position: tuple = xy
            else:
                break

    def draw(self, surface):
        """Метод для отрисовки объекта."""
        self.generate_rect(surface, self.position, color=self.body_color)


class Apple(Food):
    """Класс представляет яблоко, которое змейка может съесть."""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)


class Banana(Food):
    """Класс представляет банан, который змейка может съесть."""

    def __init__(self):
        """Инициализация атрибутов класса Банана."""
        super().__init__(body_color=BANANA_COLOR)


class Rock(Food):
    """Класс представляет камень, на который змейка может наткнуться."""

    def __init__(self):
        """Инициализация атрибутов дочернего класса Камня."""
        super().__init__(body_color=ROCK_COLOR)


class Snake(GameObject):
    """Класс представляет змейку, которой управляет игрок."""

    def __init__(self):
        """Инициализация атрибутов класса Змейки."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self, new_direction=None):
        """
        Метод для обновления направления
        после нажатия на направляющую кнопку.
        """
        if new_direction:
            self.direction: tuple = new_direction

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
            screen.fill(BOARD_BACKGROUND_COLOR)
        else:
            self.positions.insert(0, new_head_position)
            if len(self.positions) > self.length:
                self.last = self.positions.pop()

    def draw(self, surface):
        """Метод для отрисовки объекта."""
        for position in self.positions:
            self.generate_rect(surface, position, self.body_color)

        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            self.generate_rect(surface, last_rect, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод для получения позиции головы земейки."""
        return self.positions[0]

    def reset(self):
        """Метод для сброса змейки в начальное состояние."""
        self.length: int = 1
        self.last: Optional[tuple] = None
        self.next_direction: Optional[tuple] = None
        self.direction = RIGHT
        self.positions = [self.position]
        # if len(self.positions) > 1:
        #     del self.positions[1:]


def handle_keys(game_object):
    """Обработка нажатия клавиш."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit
            return CONTROL_DICT.get(
                (game_object.direction, event.key),
                game_object.direction
            )


def main():
    """Основная функция игры с бесконечным циклом."""
    apple = Apple()
    snake = Snake()
    banana = Banana()
    rock = Rock()
    while True:
        clock.tick(SPEED)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.update_direction(handle_keys(snake))

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)
        if snake.get_head_position() == rock.position:
            rock.randomize_position(snake.positions)
            snake.reset()
        if snake.get_head_position() == banana.position:
            banana.randomize_position(snake.positions)
            if len(snake.positions) > 1:
                snake.length -= 1
                snake.last = snake.positions.pop()
            elif len(snake.positions) == 1:
                snake.reset()

        snake.draw(screen)
        snake.move()
        apple.draw(screen)
        banana.draw(screen)
        rock.draw(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
