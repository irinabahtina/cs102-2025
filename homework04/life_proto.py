import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        """Отрисовать сетку"""
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        # Мой код:
        self.grid = self.create_grid(randomize=True)

        # Добавляем переменную для паузы
        paused = False
        running = True

        while running:
            # Обработка событий
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            # Очищаем экран каждый кадр
            self.screen.fill(pygame.Color("white"))

            # Рисуем клетки
            self.draw_grid()

            # Рисуем сетку поверх клеток
            self.draw_lines()

            # Выполняем шаг игры (если не на паузе)
            if not paused:
                self.grid = self.get_next_generation()

            # Обновляем экран
            pygame.display.flip()

            # Контроль скорости
            clock.tick(self.speed)

        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.

        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.

        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.

        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        # Мой код:

        grid = []  # Создаем пустой список для сетки

        for row in range(self.cell_height):  # Проходим по всем строкам
            row_cells = []  # Создаем новую строку
            for col in range(self.cell_width):  # Проходим по всем столбцам
                if randomize:
                    # Случайное значение 0 или 1 (мертвая или живая)
                    cell_value = random.randint(0, 1)
                else:
                    # Все клетки мертвые (значение 0)
                    cell_value = 0
                row_cells.append(cell_value)  # Добавляем клетку в строку
            grid.append(row_cells)  # Добавляем строку в сетку

        return grid  # Возвращаем созданную сетку

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        # Мой код:

        for row in range(self.cell_height):  # Проходим по всем строкам
            for col in range(self.cell_width):  # Проходим по всем столбцам
                if self.grid[row][col] == 1:  # Если клетка живая
                    # Вычисляем координаты для отрисовки клетки
                    x = col * self.cell_size  # X-координата левого края
                    y = row * self.cell_size  # Y-координата верхнего края

                    # создаём прямоугольник для клетки
                    cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)

                    # сначала закрашиваем фон клетки (мертвая = белый)
                    if self.grid[row][col] == 0:  # Если клетка мертвая
                        pygame.draw.rect(
                            self.screen,
                            pygame.Color("white"),  # Белый цвет для мертвых клеток
                            cell_rect,
                        )
                    else:  # Если клетка живая
                        pygame.draw.rect(
                            self.screen,
                            pygame.Color("palegreen"),  # цвет для живых клеток
                            cell_rect,
                        )

                    # Рисуем границу клетки
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("black"),
                        cell_rect,
                        1,  # Толщина границы
                    )

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.

        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.

        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.

        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        # Мой код:

        row, col = cell  # Распаковываем координаты клетки
        neighbours = []  # Создаем пустой список для значений соседей

        # Перебираем всех соседей в радиусе 1 клетки (квадрат 3x3)
        for i in range(-1, 2):  # i = -1, 0, 1
            for j in range(-1, 2):  # j = -1, 0, 1
                if i == 0 and j == 0:  # Пропускаем саму клетку
                    continue

                # Вычисляем координаты соседа
                neighbour_row = row + i
                neighbour_col = col + j

                # Проверяем, что сосед находится в пределах поля
                if 0 <= neighbour_row < self.cell_height and 0 <= neighbour_col < self.cell_width:
                    # Добавляем значение соседа в список
                    neighbours.append(self.grid[neighbour_row][neighbour_col])

        return neighbours  # Возвращаем список значений всех соседей

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        # Мой код:

        # Создаем новую пустую сетку такого же размера
        new_grid = self.create_grid(randomize=False)

        # Проходим по всем клеткам текущей сетки
        for row in range(self.cell_height):
            for col in range(self.cell_width):
                # Получаем список значений соседей текущей клетки
                neighbours = self.get_neighbours((row, col))

                # Считаем количество живых соседей (значение 1)
                alive_neighbours = sum(neighbours)

                # Применяем правила игры "Жизнь"
                if self.grid[row][col] == 1:  # Если клетка живая
                    if alive_neighbours == 2 or alive_neighbours == 3:
                        # Клетка остается живой (2 или 3 живых соседа)
                        new_grid[row][col] = 1
                    else:
                        # Клетка умирает (одиночество или перенаселение)
                        new_grid[row][col] = 0
                else:  # Если клетка мертвая
                    if alive_neighbours == 3:
                        # Клетка оживает (ровно 3 живых соседа)
                        new_grid[row][col] = 1
                    else:
                        # Клетка остается мертвой
                        new_grid[row][col] = 0

        return new_grid  # Возвращаем новое поколение


if __name__ == "__main__":
    frog = GameOfLife()
    frog.run()
