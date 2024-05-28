class Settings:
    def __init__(self):
        self.W = 1000
        self.H = 700
        self.bg_color = (83, 104, 114)

        self.alien_speed = 0.1
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        self.ship_speed = 1
        self.ship_limit = 3

        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # темп ускорения игры
        self.speedup_scale = 1.1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # инициализирует настройки, изменяющиеся в ходе игры
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3.0
        self.alien_speed_factor = 1.0

        # fleet_direction = 1 обозначает движение вправо, а -1 - влево
        self.fleet_direction = 1

        # подсчет очков
        self.alien_points = 50

    def increase_speed(self):
        # увеличивает настройки скорости
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
