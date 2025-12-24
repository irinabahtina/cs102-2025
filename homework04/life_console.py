import curses

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """Отобразить рамку."""
        # мой код:

        # Получаем размеры терминала (высота и ширина)
        height, width = screen.getmaxyx()

        # отступаем от краёв на 1 символ, чтобы не выйти за границы
        # Рисуем горизонтальные границы (верхнюю и нижнюю)
        for x in range(1, width - 2):  # Изменено: width - 2 вместо width - 1
            screen.addch(0, x, "-")  # Верхняя граница
            screen.addch(height - 2, x, "-")  # Нижняя граница (height - 2 вместо height - 1)

        # Рисуем вертикальные границы (левую и правую)
        for y in range(1, height - 2):  # Изменено: height - 2 вместо height - 1
            screen.addch(y, 0, "|")  # Левая граница
            screen.addch(y, width - 2, "|")  # Правая граница (width - 2 вместо width - 1)

        # Рисуем углы рамки
        screen.addch(0, 0, "+")
        screen.addch(0, width - 2, "+")  # width - 2
        screen.addch(height - 2, 0, "+")  # height - 2
        screen.addch(height - 2, width - 2, "+")  # width - 2 и height - 2

    def draw_grid(self, screen) -> None:
        """Отобразить состояние клеток."""
        # мой код:

        # Получаем размеры поля
        rows, cols = self.life.rows, self.life.cols
        screen_height, screen_width = screen.getmaxyx()

        # Учитываем рамку. Отступаем на 1 от краёв
        usable_height = screen_height - 2  # Минус верхняя и нижняя граница
        usable_width = screen_width - 2  # Минус левая и правая граница

        # Рассчитываем позицию для отрисовки по центру
        start_y = max(1, (usable_height - rows) // 2)
        start_x = max(1, (usable_width - cols) // 2)

        # Проверяем, помещается ли поле (теперь с учётом рамки)
        if start_y + rows >= usable_height or start_x + cols >= usable_width:
            error_msg = "Окно слишком мало!"
            if usable_width > len(error_msg):
                screen.addstr(1, 1, error_msg)
            return

        # Отрисовываем клетки
        for y in range(rows):
            for x in range(cols):
                screen_y = start_y + y
                screen_x = start_x + x
                # Проверяем границы без учета крайних символов
                if screen_y < usable_height and screen_x < usable_width:
                    # Живые клетки - символ '■', мертвые - пробел
                    if self.life.curr_generation[y][x] == 1:
                        screen.addch(screen_y, screen_x, "■")
                    else:
                        screen.addch(screen_y, screen_x, " ")

    def run(self) -> None:
        screen = curses.initscr()
        # мой код:

        # Настраиваем curses
        curses.curs_set(0)  # Скрываем курсор
        screen.nodelay(True)  # Неблокирующий ввод (было 1, теперь True)
        screen.timeout(100)  # Таймаут 100 мс

        try:
            # Основной игровой цикл
            while True:
                # Очищаем экран
                screen.clear()

                # Рисуем рамку и сетку
                self.draw_borders(screen)
                self.draw_grid(screen)

                # Получаем размеры с учётом рамки
                height, width = screen.getmaxyx()
                usable_width = width - 2

                # Добавляем информацию (проверяем, чтобы не выйти за границы)
                gen_text = f"Поколение: {self.life.generations}"
                if len(gen_text) < usable_width:
                    screen.addstr(0, 1, gen_text)  # Сдвигаем на 1 от левого края

                # Инструкции
                instr_text = "q: выход, пробел: пауза"
                if len(instr_text) < usable_width:
                    screen.addstr(1, 1, instr_text)  # Сдвигаем на 1 от левого края

                # Обновляем экран
                screen.refresh()

                # Обрабатываем нажатия клавиш
                key = screen.getch()
                if key == ord("q"):  # Выход по клавише 'q'
                    break
                elif key == ord(" "):  # Пауза по пробелу
                    # Ждем следующего нажатия пробела
                    while True:
                        key = screen.getch()
                        if key == ord(" "):  # Продолжить
                            break
                        elif key == ord("q"):  # Выход во время паузы
                            return

                # Выполняем шаг игры
                self.life.step()

                # Проверяем условия окончания (также с учётом границ)
                if self.life.is_max_generations_exceeded:
                    end_text = "Максимальное число поколений достигнуто!"
                    if len(end_text) < usable_width:
                        screen.addstr(2, 1, end_text)  # Сдвигаем на 1
                    screen.refresh()
                    curses.napms(2000)
                    break
                elif not self.life.is_changing:
                    end_text = "Игра окончена!"
                    if len(end_text) < usable_width:
                        screen.addstr(2, 1, end_text)  # Сдвигаем на 1
                    screen.refresh()
                    curses.napms(2000)
                    break
        finally:
            # Всегда завершаем curses
            curses.endwin()


def main():
    """Функция для запуска консольной версии"""
    try:
        # Создаем игру с нужным размером
        # Размеры поля должны быть меньше размеров вашего терминала
        life = GameOfLife((20, 40), randomize=True, max_generations=100)

        # Создаем консольный интерфейс
        console = Console(life)

        # Запускаем игру
        console.run()

    except curses.error:
        print("Ошибка: окно терминала слишком маленькое!")
        print("Увеличьте размер окна терминала и попробуйте снова.")
    except KeyboardInterrupt:
        print("\nИгра остановлена пользователем.")
    except Exception as e:
        print(f"Ошибка: {e}")
    print("Игра завершена.")


if __name__ == "__main__":
    main()
