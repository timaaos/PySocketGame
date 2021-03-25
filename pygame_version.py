import pygame
from settings import Settings
from board import draw
from game_functions import check_events
from character import Character

if __name__ == '__main__':
    """Создаем окно в pygame"""
    pygame.init()
    settings = Settings()
    size = width, height = settings.width, settings.height
    screen = pygame.display.set_mode(size)

    """Главный игровой цикл"""
    running = True
    clock = pygame.time.Clock()
    pos = x, y = 0, 0
    character = Character(screen, x, y)
    while running:
        running = check_events()
        # Рисуем поле
        draw(screen)
        character.blitme()
        pygame.display.flip()
        clock.tick(settings.fps)
    pygame.quit()
