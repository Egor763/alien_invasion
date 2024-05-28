import pygame.font


class Scoreboard:
    # класс для вывода игровой информации
    def __init__(self, ai_game):
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # настройки шрифта для вывода счета
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # подготовка исходного изображения
        self.prep_score()

    def prep_score(self):
        # преобразует текущий счет в графическое изображение
        score_str = str(self.stats.score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )

        # вывод счета в правой верхней части экрана
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        # выводит счет на экран
        self.screen.blit(self.score_image, self.score_rect)
