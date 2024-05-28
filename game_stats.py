class GameStats:
    # отслеживание статистики для игры Alien Invasion

    def __init__(self, ai_game):
        # инициализирует статистику
        self.settings = ai_game.settings
        self.reset_stats()

        # игра запускается в неактивном состоянии
        self.game_active = False

    def reset_stats(self):
        # инициализирует статистику, изменяющуюся в ходе игры
        self.ships_left = self.settings.ship_limit
        self.score = 0