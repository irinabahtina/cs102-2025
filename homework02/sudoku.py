import pathlib
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    """Прочитать Судоку из указанного файла"""
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print("".join(grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)))
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов
    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i + n] for i in range(0, len(values), n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера строки, указанной в pos
    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения для номера столбца, указанного в pos
    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    _, col = pos
    return [row[col] for row in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    """Возвращает все значения из квадрата, в который попадает позиция pos
    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row, col = pos
    # Определяем начало блока 3x3
    block_row = (row // 3) * 3
    block_col = (col // 3) * 3

    values = []
    for i in range(block_row, block_row + 3):
        for j in range(block_col, block_col + 3):
            values.append(grid[i][j])
    return values


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    """Найти первую свободную позицию в пазле
    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for i, row in enumerate(grid):
        for j, value in enumerate(row):
            if value == ".":
                return (i, j)
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    """Вернуть множество возможных значения для указанной позиции
    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    row, col = pos

    # Если позиция уже заполнена, возвращаем пустое множество
    if grid[row][col] != ".":
        return set()

    # Все возможные значения от 1 до 9
    all_values = set("123456789")

    # Убираем значения, которые уже есть в строке
    row_values = set(get_row(grid, pos)) - {"."}

    # Убираем значения, которые уже есть в столбце
    col_values = set(get_col(grid, pos)) - {"."}

    # Убираем значения, которые уже есть в блоке
    block_values = set(get_block(grid, pos)) - {"."}

    # Объединяем все использованные значения
    used_values = row_values.union(col_values).union(block_values)

    # Возвращаем разность между всеми возможными и использованными значениями
    return all_values - used_values


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    """Решение пазла, заданного в grid"""
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла
    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    # Находим первую свободную позицию
    empty_pos = find_empty_positions(grid)

    # Если свободных позиций нет, значит пазл решен
    if not empty_pos:
        return grid

    row, col = empty_pos

    # Находим возможные значения для этой позиции
    possible_values = find_possible_values(grid, empty_pos)

    # Перебираем все возможные значения
    for value in possible_values:
        # Пробуем поставить значение
        grid[row][col] = value

        # Рекурсивно решаем оставшуюся часть
        solution = solve(grid)

        # Если решение найдено, возвращаем его
        if solution:
            return solution

        # Если решение не найдено, откатываем изменения
        grid[row][col] = "."

    # Если ни одно значение не подошло, возвращаем None
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    """Если решение solution верно, то вернуть True, в противном случае False"""
    # TODO: Add doctests with bad puzzles
    if not solution:
        return False

        # Проверяем, что все строки содержат цифры 1-9 без повторений
    for i in range(9):
        row = get_row(solution, (i, 0))
        if set(row) != set("123456789"):
            return False

        # Проверяем, что все столбцы содержат цифры 1-9 без повторений
    for j in range(9):
        col = get_col(solution, (0, j))
        if set(col) != set("123456789"):
            return False

        # Проверяем, что все блоки 3x3 содержат цифры 1-9 без повторений
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            block = get_block(solution, (i, j))
            if set(block) != set("123456789"):
                return False

    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов
    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    # Создаем полностью заполненное корректное судоку
    # Можно использовать простое решение - начать с известного правильного судоку
    # и удалить нужное количество элементов

    import random

    # Создаём пустую сетку
    grid = [['.' for _ in range(9)] for _ in range(9)]

    # Заполняем диагональные блоки 3x3 (они независимы друг от друга)
    for block_row in range(0, 9, 3):
        numbers = list("123456789")
        random.shuffle(numbers)
        for i in range(3):
            for j in range(3):
                grid[block_row + i][block_row + j] = numbers[i * 3 + j]

    # Решаем полученный пазл
    solution = solve([row[:] for row in grid])  # создаем копию

    if not solution:
        # Если не удалось решить, возвращаем пустую сетку
        return [['.' for _ in range(9)] for _ in range(9)]

    # Ограничиваем N в диапазоне 0-81
    N = max(0, min(81, N))

    # Количество позиций, которые нужно оставить пустыми
    empty_count = 81 - N

    # Список всех позиций
    positions = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(positions)

    # Создаем копию решения и заменяем некоторые цифры точками
    result = [row[:] for row in solution]

    # Очищаем первые empty_count позиций
    for k in range(empty_count):
        if k < len(positions):
            i, j = positions[k]
            result[i][j] = "."

    return result


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
