import pygame
from settings import Settings
from ship import Ship


# Класс для управлениями ресурсами и поведением игры
class AlienInvasion:
    # инициализирует игру и создает новые игровые ресурсы
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.W, self.settings.H))
        pygame.display.set_caption("Инопланетное вторжение")

        self.ship = Ship(self)

    def run_game(self):
        # запуск основного цикла игры
        while True:
            self.ship.update()
            # ослеживание событий клавиатуры и мыши
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = True

                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = True

                    elif event.key == pygame.K_q:
                        exit()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False

                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = False

            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()
            # отображение последнего прорисованного экрана
            pygame.display.flip()


if __name__ == "__main__":
    # создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
