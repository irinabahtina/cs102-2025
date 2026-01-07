from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union

import pandas as pd


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    # Выбираем направление: наверх или направо
    direction = choice(["up", "right"])

    # Если в выбранном направлении следующая клетка за границами, выбираем другое
    if direction == "up" and x - 2 < 0:  # Нельзя пойти наверх
        direction = "right"
    elif direction == "right" and y + 2 >= len(grid[0]):  # Нельзя пойти направо
        direction = "up"

    # Убираем стену
    if direction == "up" and x - 2 >= 0:
        grid[x - 1][y] = " "
    elif direction == "right" and y + 2 < len(grid[0]):
        grid[x][y + 1] = " "

    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    # Реализация алгоритма двоичного дерева
    for cell in empty_cells:
        grid = remove_wall(grid, cell)

        # генерация входа и выхода
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    exits = []
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == "X":
                exits.append((i, j))
    return exits


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    # Реализация шага волнового алгоритма
    rows = len(grid)
    cols = len(grid[0])

    # Создаем копию сетки
    new_grid = deepcopy(grid)

    # Ищем все клетки с номером k
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == k:
                # Проверяем 4 направления
                for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    ni, nj = i + dx, j + dy
                    if 0 <= ni < rows and 0 <= nj < cols:
                        # Если соседняя клетка пустая (0) или это выход (пока еще "X")
                        if grid[ni][nj] == 0 or grid[ni][nj] == "X":
                            new_grid[ni][nj] = k + 1

    return new_grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x, y = exit_coord

    # Проверяем, что выход достижим
    if not isinstance(grid[x][y], int) or grid[x][y] <= 0:
        return None

    # Находим вход (клетка со значением 1)
    entrance = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                entrance = (i, j)
                break
        if entrance:
            break

    if not entrance:
        return None

    # Восстанавливаем путь от выхода ко входу
    path = [(x, y)]
    current_x, current_y = x, y
    current_value = grid[x][y]

    while (current_x, current_y) != entrance and current_value > 1:
        found = False
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = current_x + dx, current_y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                if isinstance(grid[nx][ny], int) and grid[nx][ny] == current_value - 1:
                    path.append((nx, ny))
                    current_x, current_y = nx, ny
                    current_value = grid[nx][ny]
                    found = True
                    break

        if not found:
            return None

        # Добавляем вход в путь, только если еще не добавили
    if (current_x, current_y) != entrance:
        path.append(entrance)

        # Возвращаем путь от выхода ко входу
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    x, y = coord
    rows = len(grid)
    cols = len(grid[0])

    # Если клетка не на границе - сразу False
    if not (x == 0 or x == rows - 1 or y == 0 or y == cols - 1):
        return False

    # Проверяем всех соседей
    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nx, ny = x + dx, y + dy

        # Если сосед в пределах сетки
        if 0 <= nx < rows and 0 <= ny < cols:
            # Если хоть один сосед не стена - выход не окружен
            if grid[nx][ny] != "■":
                return False

    # Все существующие соседи - стены и выход на границе
    return True


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """

    :param grid:
    :return:
    """

    # 1. проверяем, что выходов больше одного
    exits = get_exits(grid)

    if len(exits) < 2:
        # Если только один выход - это и есть путь
        return grid, (exits[0] if exits else None)

    # 2. проверяем, что мы не в тупике (выход не окружен стенами)
    for exit_coord in exits:
        if encircled_exit(grid, exit_coord):
            return grid, None

    # 3. реализуем алгоритм Дейкстры (волновой алгоритм)

    # Создаем копию лабиринта для работы
    maze_copy = deepcopy(grid)

    # Подготавливаем лабиринт: пустые клетки -> 0, стены -> -1
    for i in range(len(maze_copy)):
        for j in range(len(maze_copy[0])):
            if maze_copy[i][j] == " ":
                maze_copy[i][j] = 0
            elif maze_copy[i][j] == "■":
                maze_copy[i][j] = -1
            # Выходы пока оставляем как "X"

    # Определяем вход и выход
    entrance = exits[0]
    exit_point = exits[1]

    # В клетку входа вместо крестика ставим 1
    maze_copy[entrance[0]][entrance[1]] = 1

    k = 1
    max_steps = len(maze_copy) * len(maze_copy[0])

    # Пока в клетке выхода лежит 0 или "X"
    for _ in range(max_steps):
        # Проверяем, достигли ли выхода
        exit_val = maze_copy[exit_point[0]][exit_point[1]]
        if isinstance(exit_val, int) and exit_val > 0:
            break

        # Сохраняем предыдущее состояние
        prev_state = deepcopy(maze_copy)

        # Делаем шаг волнового алгоритма
        maze_copy = make_step(maze_copy, k)

        # Если состояние не изменилось - выходим
        if maze_copy == prev_state:
            break

        k += 1

    # Проверяем, нашли ли путь
    exit_val = maze_copy[exit_point[0]][exit_point[1]]
    if isinstance(exit_val, int) and exit_val > 0:
        # Восстанавливаем путь
        path = shortest_path(maze_copy, exit_point)
        return maze_copy, path
    else:
        return maze_copy, None


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid


if __name__ == "__main__":
    print(pd.DataFrame(bin_tree_maze(15, 15)))
    GRID = bin_tree_maze(15, 15)
    print(pd.DataFrame(GRID))
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
    print(pd.DataFrame(MAZE))
