import pygame
from pygame.sprite import Sprite
from settings import Settings

# from ship import Ship


class Bullet(Sprite):
    # Класс для управления снарядами, выпущенными кораблями
    def __init__(self, screen, ship):
        # Создает объект снарядов в текущей позиции корабля
        super().__init__()
        self.screen = screen
        self.settings = Settings()
        # self.ship = Ship(screen)
        self.color = self.settings.bullet_color

        self.ship = ship

        # Создание снаряда в позиции (0, 0) и назначение начальной позиции
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height
        )
        self.rect.midtop = self.ship.rect.midtop

        # Позиция снаряда хранится в вещественном формате
        self.y = float(self.rect.y)

    def update(self):
        # Перемещает снаряд вверх по экрану
        self.y -= self.settings.bullet_speed
        # Обновление позиции прямоугольника
        self.rect.y = self.y

    def draw_bullet(self):
        # Вывод снаряда на экран
        pygame.draw.rect(self.screen, self.color, self.rect)
