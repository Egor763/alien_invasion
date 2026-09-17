import pygame


class Ship:
    # Класс для управления корабля
    def __init__(self, screen):
        self.screen = screen
        # Инициализирует корабль и задает его начальную позицию

        self.screen_rect = screen.get_rect()

        # Загружает изображение корабля и получает прямоугольник
        self.image = pygame.image.load("images/ship.png")
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.moving_right = False
        self.moving_left = False

    def blitme(self):
        # Рисует корабль в текущей позиции
        self.screen.blit(self.image, self.rect)

    def update(self):
        # Обновляет позицию корабля с учетом флага
        if self.moving_right:
            self.rect.x += 1

        if self.moving_left:
            self.rect.x -= 1
