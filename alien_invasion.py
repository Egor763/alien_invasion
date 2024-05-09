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

        # self.aliens.add(self.alien)
        self.create_fleet()

    def update_aliens(self):
        self.check_fleet_edges()
        self.aliens.update()

    def update_bullets(self):
        self.bullets.update()
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)
        if not self.aliens:
            self.bullets.empty()
            self.create_fleet()

    def check_fleet_edges(self):
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def screen_update(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        pygame.display.flip()

    def create_fleet(self):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.W - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        ship_height = self.ship.rect.height
        available_space_y = self.settings.H - (3 * alien_height) - ship_height

        number_rows = available_space_y // (2 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self.create_alien(alien_number, row_number)

    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def run_game(self):
        # запуск основного цикла игры

        while True:
            self.ship.update()
            self.update_bullets()
            self.update_aliens()

            self.screen_update()

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

            # self.create_fleet()

            def fire_bullet(self):
                if len(self.bullets) < self.settings.bullets_allowed:
                    new_bullet = Bullet(self)
                    self.bullets.add(new_bullet)

            # pygame.display.flip()

            # отображение последнего прорисованного экрана
            # pygame.display.flip()


if __name__ == "__main__":
    # создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
