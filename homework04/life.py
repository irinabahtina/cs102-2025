import pathlib
import random
import typing as tp

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        # Создание сетки клеток.
        # мой код:

        grid = []  # Создаем пустой список для сетки

        for row in range(self.rows):  # Проходим по всем строкам
            row_cells = []  # Создаем новую строку
            for col in range(self.cols):  # Проходим по всем столбцам
                if randomize:
                    # Случайное значение: 1 (живая) или 0 (мертвая)
                    cell_value = random.randint(0, 1)
                else:
                    # Все клетки мертвые (значение 0)
                    cell_value = 0
                row_cells.append(cell_value)  # Добавляем клетку в строку
            grid.append(row_cells)  # Добавляем строку в сетку

        return grid  # Возвращаем созданную сетку

    def get_neighbours(self, cell: Cell) -> Cells:
        # Вернуть список соседних клеток для клетки cell
        # мой код:

        row, col = cell  # Распаковываем координаты клетки
        neighbours = []  # Создаем пустой список для значений соседей

        # Перебираем всех соседей в квадрате 3x3 вокруг клетки
        for i in range(-1, 2):  # i = -1, 0, 1 (смещение по строкам)
            for j in range(-1, 2):  # j = -1, 0, 1 (смещение по столбцам)
                if i == 0 and j == 0:  # Пропускаем саму клетку
                    continue

                # Вычисляем координаты соседа
                neighbour_row = row + i
                neighbour_col = col + j

                # Проверяем, что сосед находится в пределах поля
                if 0 <= neighbour_row < self.rows and 0 <= neighbour_col < self.cols:
                    # Добавляем значение соседа в список
                    neighbours.append(self.curr_generation[neighbour_row][neighbour_col])

        return neighbours  # Возвращаем список значений всех соседей

    def get_next_generation(self) -> Grid:
        # Получение списка соседей для клетки.
        # мой код:

        # Создаем новую пустую сетку такого же размера
        new_grid = self.create_grid(randomize=False)

        # Проходим по всем клеткам текущей сетки
        for row in range(self.rows):
            for col in range(self.cols):
                # Получаем список значений соседей текущей клетки
                neighbours = self.get_neighbours((row, col))

                # Считаем количество живых соседей (значение 1)
                alive_neighbours = sum(neighbours)

                # Применяем правила игры "Жизнь"
                current_cell = self.curr_generation[row][col]

                if current_cell == 1:  # Если клетка живая
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

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        # мой код:

        # Сохраняем текущее поколение как предыдущее (глубокое копирование)
        self.prev_generation = [row[:] for row in self.curr_generation]

        # Получаем следующее поколение
        self.curr_generation = self.get_next_generation()

        # Увеличиваем счетчик поколений
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        # мой код:

        # Сравниваем текущее число поколений с максимальным
        # Возвращаем True, если поколений больше или равно максимальному
        return self.generations >= self.max_generations

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        # мой код:

        # Сравниваем текущее и предыдущее поколение поэлементно
        for row in range(self.rows):
            for col in range(self.cols):
                # Если нашли хотя бы одну различающуюся клетку
                if self.curr_generation[row][col] != self.prev_generation[row][col]:
                    return True  # Состояние изменилось

        # Все клетки одинаковые - состояние не изменилось
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла.
        """
        # мой код:

        with open(filename, "r") as f:  # Открываем файл для чтения
            lines = f.readlines()  # Читаем все строки файла

        # Убираем символы новой строки и лишние пробелы
        lines = [line.strip() for line in lines if line.strip()]

        # Определяем размер поля
        rows = len(lines)  # Количество строк = количество строк в файле
        cols = len(lines[0])  # Количество столбцов = длина первой строки

        # Создаем экземпляр игры с нужным размером (все клетки мертвые)
        game = GameOfLife((rows, cols), randomize=False)

        # Заполняем поле значениями из файла
        for i, line in enumerate(lines):  # i - номер строки, line - строка из файла
            for j, char in enumerate(line):  # j - номер столбца, char - символ
                # Преобразуем символ в число: '1' или '*' -> 1, все остальное -> 0
                game.curr_generation[i][j] = 1 if char in "1*" else 0

        # Обнуляем предыдущее поколение
        game.prev_generation = game.create_grid(randomize=False)

        # Сбрасываем счетчик поколений
        game.generations = 1

        return game  # Возвращаем созданную игру


def save(self, filename: pathlib.Path) -> None:
    """
    Сохранить текущее состояние клеток в указанный файл.
    """
    # мой код:

    with open(filename, "w") as f:  # Открываем файл для записи
        for row in self.curr_generation:  # Проходим по всем строкам поля
            # Преобразуем каждую клетку в строку: 1 -> '1', 0 -> '0'
            line = "".join(str(cell) for cell in row)
            f.write(line + "\n")  # Записываем строку в файл с переводом строки
