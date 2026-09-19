from time import sleep

import pygame

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    # Класс для управления ресурсами и поведения игры
    def __init__(self):
        # Инициализирует игру и создает игровые ресурсы
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.W = self.screen.get_rect().width
        self.settings.H = self.screen.get_rect().height
        pygame.display.set_caption("Инопланетное вторжение")

        self.stats = GameStats()

        screen = self.screen

        self.ship = Ship(screen)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

    def run_game(self):
        # Запуск основного цикла игры
        while True:
            # Отслеживание событий клавиатуры и мыши

            self._check_events()
            self.ship.update()

            self._update_bullets()
            self._update_aliens()

            self._update_screen()

    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)

            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Реагирует на нажатие клавиш
        if event.key == pygame.K_RIGHT:
            # Переместить корабль вправо
            self.ship.moving_right = True
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                self.ship.rect.x += 10

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True

        elif event.key == pygame.K_q:
            exit()

        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        # Реагирует на отпускание клавиш
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False

        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # Создание нового снаряда и включение его в группу bullets
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self.screen, self.ship)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        self.bullets.update()

        # Проверка попаданий в пришельцев
        # При обнаружении попадания удалить снаряд и пришельца

        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

            self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # Обработка коллизий снарядов с пришельцами
        # Удаление снарядов и пришельцев, учавствующих в коллизиях
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if not self.aliens:
            # Уничтожение существующих снарядов и восстановление флота
            self.bullets.empty()
            self._create_fleet()

    def _update_aliens(self):
        # Обновляет позиции всех пришельцев во флоте
        if self._check_fleet_edges():
            self._change_fleet_direction()

        for alien in self.aliens.sprites():
            alien.x += self.settings.alien_speed * self.settings.fleet_direction
        self.aliens.update()

        # Проверка коллизий "пришелец - корабль"
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_fleet_edges(self):
        # Реагирует на достижение пришельцем края экрана

        for alien in self.aliens.sprites():
            if alien.check_edges():
                # self._change_fleet_direction()
                return True

        return False

    def _change_fleet_direction(self):
        # Опускает весь флот и меняет направление флота
        self.settings.fleet_direction *= -1
        # Опускаем весь флот вниз
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
            # И сразу "прижимаем" к границе, чтобы не улетели
            screen_rect = self.screen.get_rect()
            if alien.rect.right > screen_rect.right:
                alien.rect.right = screen_rect.right
                alien.x = float(alien.rect.x)

            elif alien.rect.left < 0:
                alien.rect.left = 0
                alien.x = float(alien.rect.x)

    def _create_fleet(self):
        alien = Alien(self.screen)
        alien_width, alien_height = alien.rect.size
        ship_height = self.ship.rect.height

        # Небольшой отступ сверху (чтобы флот не прилипал к краю экрана)
        top_margin = 20

        available_space_x = self.settings.W - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Считаем свободное место: экран минус отступ сверху и место под корабль
        available_space_y = self.settings.H - top_margin - ship_height

        # Шаг между рядами: высота пришельца + небольшой зазор
        row_step = (
            alien_height + 10
        )  # можно поставить 10, 15 или 20 — как больше нравится
        number_rows = available_space_y // row_step

        print(
            f"top_margin={top_margin}, row_step={row_step}, number_rows={number_rows}"
        )

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        # Создание пришельца и размещение его в ряду
        alien = Alien(self.screen)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x

        top_margin = 20
        row_step = alien_height + 10

        alien.y = top_margin + row_step * row_number
        alien.rect.y = alien.y
        self.aliens.add(alien)

    def _ship_hit(self):
        # Обрабатывает столкновение корабля с пришельцем
        # Уменьшение ships_left
        self.stats.ships_left -= 1

        # Очистка списков пришельцев и снарядов
        self.aliens.empty()
        self.bullets.empty()

        # Создание нового флота и размещение корабля в центре
        self._create_fleet()
        self.ship.center_ship()

        # Пауза
        sleep(0.5)

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)

        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        # Отслеживание последнего прорисованного экрана
        pygame.display.flip()


if __name__ == "__main__":
    # Создание экземпляра и запуск игры
    ai = AlienInvasion()
    ai.run_game()
