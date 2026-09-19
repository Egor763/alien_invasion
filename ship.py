import pygame

from settings import Settings


class Ship:
    # Класс для управления корабля
    def __init__(self, screen):
        self.screen = screen
        # Инициализирует корабль и задает его начальную позицию
        self.screen_rect = self.screen.get_rect()

        self.settings = Settings()

        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom

        # Сохранение вещественной координаты центра корабля
        self.x = float(self.rect.x)

        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        # Рисует корабль в текущей позиции
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Обновляет позицию корабля с учетом флага
        # Обновляется атрибут x, не rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed

        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = int(self.x)

    def center_ship(self):
        # Размещает корабль в центре нижней стороны
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
