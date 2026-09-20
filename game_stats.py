from settings import Settings


class GameStats:
    # Отслеживание статистики для игры Alien Invasion
    def __init__(self):
        # Инициализирует стаитстику
        self.settings = Settings()
        self.reset_stats()

        # Игра Alien Invasion запускается в активном состоянии
        self.game_active = True

    def reset_stats(self):
        # Инициализирует статистику, изменяющуюся в ходе игры
        self.ships_left = self.settings.ship_limit
