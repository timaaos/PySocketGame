import pygame
from settings import Settings


def draw(screen):
    settings = Settings()
    pygame.draw.rect(screen, (6, 214, 103), (0, 0, settings.width, settings.height - settings.height * 0.10), 0)
