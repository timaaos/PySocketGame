import pygame
from settings import Settings
from game_functions import check_events, update_screen
from character import Character

if __name__ == '__main__':
    """Создаем окно в pygame"""
    pygame.init()
    settings = Settings()
    size = width, height = settings.width, settings.height - 50
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    """Главный игровой цикл"""
    clock = pygame.time.Clock()
    pos = x, y = (settings.width - settings.admin_width) // 2, 0
    character = Character(screen, x, y)
    while True:
        check_events(screen, character)
        character.update()
        # Рисуем поле
        update_screen(screen, character)
        clock.tick(settings.fps)
