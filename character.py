import pygame
from settings import Settings


class Character:
    def __init__(self, screen, x_pos, y_pos):
        self.settings = Settings()
        self.screen = screen
        self.image = pygame.image.load('images/character_for_game.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.centerx = self.screen_rect.centerx
        self.rect.x = x_pos
        self.rect.y = y_pos

    def blitme(self):
        self.screen.blit(self.image, self.rect)
