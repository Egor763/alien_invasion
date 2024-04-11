import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


# Класс для управлениями ресурсами и поведением игры
class AlienInvasion:
    # инициализирует игру и создает новые игровые ресурсы
    def __init__(self):
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.W, self.settings.H))
        pygame.display.set_caption("Инопланетное вторжение")

        self.ship = Ship(self)
        self.alien = Alien(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self.aliens.add(self.alien)

    def run_game(self):
        # запуск основного цикла игры

        while True:
            self.ship.update()

            self.bullets.update()
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)

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

                    elif event.key == pygame.K_SPACE:
                        fire_bullet(self)

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.ship.moving_right = False

                    elif event.key == pygame.K_LEFT:
                        self.ship.moving_left = False

            def create_fleet(self):
                alien = Alien(self)
                alien_width = alien.rect.width
                avariable_space_x = self.settings.W - (2 * alien_width)
                number_aliens_x = avariable_space_x // (2 * alien_width)

                for alien_number in range(number_aliens_x):
                    alien = Alien(self)
                    alien.x = alien_width + 2 * alien_width * alien_number
                    alien.rect.x = alien.x
                    self.aliens.add(alien)

            create_fleet(self)

            def fire_bullet(self):
                if len(self.bullets) < self.settings.bullets_allowed:
                    new_bullet = Bullet(self)
                    self.bullets.add(new_bullet)

            self.screen.fill(self.settings.bg_color)
            self.ship.blitme()

            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
            self.aliens.draw(self.screen)

            pygame.display.flip()

            # отображение последнего прорисованного экрана
            pygame.display.flip()


if __name__ == "__main__":
    # создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
