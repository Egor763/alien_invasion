import pygame

from settings import Settings
from ship import Ship


class AlienInvasion:
    # Класс для управления ресурсами и поведения игры
    def __init__(self):
        # Инициализирует игру и создает игровые ресурсы
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode(self.settings.window_size)
        pygame.display.set_caption("Инопланетное вторжение")

        screen = self.screen
        self.ship = Ship(screen)

        # Назначение цвета фона

    def run_game(self):
        # Запуск основного цикла игры
        while True:
            # Отслеживание событий клавиатуры и мыши

            self.check_events()
            self.ship.update()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    # Переместить корабль вправо
                    self.ship.moving_right = True

                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.ship.moving_right = False

                elif event.key == pygame.K_LEFT:
                    self.ship.moving_left = False

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()

        # Отслеживание последнего прорисованного экрана
        pygame.display.flip()


if __name__ == "__main__":
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
