import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        # мой код:

        # Размер клетки в пикселях
        self.cell_size = cell_size

        # Скорость обновления (кадров в секунду)
        self.speed = speed

        # Вычисляем размеры окна на основе размера поля и клеток
        # Ширина окна = количество столбцов * размер клетки
        self.width = life.cols * cell_size
        # Высота окна = количество строк * размер клетки
        self.height = life.rows * cell_size

        # Инициализация Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))

        # Устанавливаем заголовок окна
        pygame.display.set_caption("Game of Life")

        # Определяем цвета для отрисовки
        self.background_color = (40, 40, 40)  # Темно-серый цвет фона
        self.grid_color = (30, 30, 30)  # Цвет линий сетки (немного темнее фона)
        self.cell_color = (220, 150, 200)  # Цвет живых клеток
        self.text_color = (200, 200, 200)  # Цвет текста (светло-серый)

        # Флаги состояния
        self.running = True
        self.paused = False

        # Шрифт для текста
        self.font = pygame.font.SysFont("Arial", 16)

    def draw_lines(self) -> None:
        """Рисуем сетку"""
        # мой код:

        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (x, 0), (x, self.height), 1)
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, self.grid_color, (0, y), (self.width, y), 1)

    def draw_grid(self) -> None:
        """Рисуем клетки (и живые, и мертвые)"""
        # мой код:

        # Проходим по всем клеткам игрового поля
        for row in range(self.life.rows):  # Для каждой строки
            for col in range(self.life.cols):  # Для каждого столбца
                # Вычисляем координаты прямоугольника для клетки на экране
                # x = столбец * размер_клетки (перевод в пиксели)
                x = col * self.cell_size
                # y = строка * размер_клетки (перевод в пиксели)
                y = row * self.cell_size

                # Закрашиваем все клетки (и живые, и мертвые)
                if self.life.curr_generation[row][col] == 1:
                    color = self.cell_color  # Живая клетка
                else:
                    color = self.background_color  # Мертвая клетка (фон)

                # Рисуем залитый прямоугольник (клетку)
                # pygame.draw.rect(surface, color, rect, width=0)
                # rect = (x, y, width, height)
                pygame.draw.rect(
                    self.screen,
                    color,  # ← Используем переменную color, которая зависит от состояния клетки
                    (x, y, self.cell_size, self.cell_size),
                )

    def handle_events(self):
        """Обработка событий клавиатуры и мыши"""
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

                elif event.key == K_SPACE:
                    self.paused = not self.paused

                elif event.key == K_r:
                    # Новая случайная игра
                    self.life.curr_generation = self.life.create_grid(randomize=True)
                    self.life.generations = 1

                elif event.key == K_c:
                    # Очистить поле
                    self.life.curr_generation = self.life.create_grid(randomize=False)
                    self.life.generations = 1

            elif event.type == MOUSEBUTTONDOWN and self.paused:
                if event.button == 1:  # Левая кнопка мыши
                    x, y = event.pos
                    col = x // self.cell_size
                    row = y // self.cell_size

                    if 0 <= row < self.life.rows and 0 <= col < self.life.cols:
                        # Инвертируем состояние клетки
                        current = self.life.curr_generation[row][col]
                        self.life.curr_generation[row][col] = 1 if current == 0 else 0

    def draw_info(self):
        """Рисует информацию о игре"""
        # Информация о поколении
        status_text = f"Поколение: {self.life.generations}"
        if self.paused:
            status_text += " (Пауза)"

        text_surface = self.font.render(status_text, True, self.text_color)
        self.screen.blit(text_surface, (10, 10))

        # Инструкции по управлению
        if self.height > 120:
            instructions = [
                "Управление:",
                "SPACE - пауза/продолжить",
                "ESC - выход",
                "R - новая случайная игра",
                "C - очистить поле",
                "ЛКМ - изменить клетку (в паузе)",
            ]

            for i, line in enumerate(instructions):
                instruction_text = self.font.render(line, True, self.text_color)
                self.screen.blit(instruction_text, (10, 35 + i * 20))

    def run(self) -> None:
        """Основной цикл"""
        # мой код
        clock = pygame.time.Clock()

        while self.running:
            self.handle_events()

            # Очистка экрана
            self.screen.fill(self.background_color)

            # Отрисовка
            self.draw_grid()
            self.draw_lines()
            self.draw_info()

            # Обновление состояния игры
            if not self.paused and self.running:
                # Проверяем условия перед шагом
                if not self.life.is_max_generations_exceeded and self.life.is_changing:
                    self.life.step()
                else:
                    # Игра завершена
                    font = pygame.font.SysFont("Arial", 24)
                    if self.life.is_max_generations_exceeded:
                        end_text = "Достигнут лимит поколений!"
                    else:
                        end_text = "Игра окончена!"

                    text = font.render(end_text, True, (255, 100, 100))
                    text_rect = text.get_rect(center=(self.width // 2, self.height // 2))
                    self.screen.blit(text, text_rect)
                    pygame.display.flip()
                    pygame.time.wait(2000)
                    self.running = False

            # Обновление экрана
            pygame.display.flip()
            clock.tick(self.speed)

        pygame.quit()


def main():
    """Функция для запуска программы"""
    # Создаем игру
    life = GameOfLife((30, 40), randomize=True, max_generations=1000)

    # Создаем и запускаем GUI
    gui = GUI(life, cell_size=15, speed=10)
    gui.run()


# запуск
if __name__ == "__main__":
    main()
