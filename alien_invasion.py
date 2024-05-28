from time import sleep

import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
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

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.ship = Ship(self)
        self.alien = Alien(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        # self.aliens.add(self.alien)
        self.create_fleet()

        # создание кнопки Play
        self.play_button = Button(self, "Play")

    def update_aliens(self):
        # вызов функции проверки границ
        self.check_fleet_edges()
        # вызов функции обновления пришельцев
        self.aliens.update()

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self.ship_hit()

        # проверить, добрались ли пришельцы до нижнего края экрана
        self.check_aliens_bottom()

    def check_aliens_bottom(self):
        # проверяет, добрались ли пришельцы до нижнего края экрана
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # происходит то же, что при столкновении с кораблем
                self.ship_hit()
                break

    def ship_hit(self):
        # обрабатывает столкновение корабля с пришельцем
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1

            # очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # создание нового флота и размещение корабля в центре
            self.create_fleet()
            self.ship.center_ship()

            # пауза
            sleep(0.5)

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def update_bullets(self):
        # вызов функции обновления пуль
        self.bullets.update()
        # удаление пуль
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self.check_bullet_alien_collisions()

    def check_bullet_alien_collisions(self):
        # удаление снарядов и пришельцев, участвующих в колизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, False, True)

        if not self.aliens:
            # уничтожение существующих снарядов и создание нового флота
            self.bullets.empty()
            self.create_fleet()
            self.settings.increase_speed()

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()

    def check_fleet_edges(self):
        # проверка границ
        for alien in self.aliens.sprites():
            if alien.check_edges():
                # изменение направления
                self.change_fleet_direction()
                break

    def change_fleet_direction(self):
        # изменение направления пришельцев
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def screen_update(self):
        # обновление экрана
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)

        # вывод информации о счете
        self.sb.show_score()

        # кнопка Play отображается в том случае, если игра неактивна
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    # функция добавления флота
    def create_fleet(self):
        # создание экземпляра класса пришельцев
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

    # функция добавления пришельца
    def create_alien(self, alien_number, row_number):
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
        self.aliens.add(alien)

    def check_play_button(self, mouse_pos):
        # запускает новую игру при нажатии кнопки Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # сброс игровых настроек
            self.settings.initialize_dynamic_settings()
            # сброс игровой статистики
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()

            # очистка списков пришельцев и снарядов
            self.aliens.empty()
            self.bullets.empty()

            # создание нового флота и размещение корабля в центре
            self.create_fleet()
            self.ship.center_ship()

            # указатель мыши скрывается
            pygame.mouse.set_visible(False)

    def run_game(self):
        # запуск основного цикла игры

        while True:
            if self.stats.game_active:
                self.ship.update()
                self.update_bullets()
                self.update_aliens()

            self.screen_update()

            # ослеживание событий клавиатуры и мыши
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self.check_play_button(mouse_pos)

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
                # вылет снаряда
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
