from settings import Settings


class GameStats:
    # Отслеживание статистики для игры Alien Invasion
    def __init__(self):
        # Инициализирует стаитстику
        self.settings = Settings()
        self.reset_stats()

    def reset_stats(self):
        # Инициализирует статистику, изменяющуюся в ходе игры
        self.ships_left = self.settings.ship_limit
