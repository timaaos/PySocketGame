import pygame
import sys
from settings import Settings


def check_down_events(event, character1):
    settings = Settings()
    if event.key == pygame.K_RIGHT and character1.rect.x + settings.speed_x * 2 < settings.width - (
            settings.width - settings.admin_width) // 2:
        character1.rect.x += settings.speed_x
        character1.centerx += settings.speed_x
    if event.key == pygame.K_LEFT and character1.rect.x - settings.speed_x >= (
            settings.width - settings.admin_width) // 2:
        character1.rect.x -= settings.speed_x
        character1.centerx -= settings.speed_x
    if event.key == pygame.K_UP and character1.rect.y - settings.speed_y >= 0:
        character1.rect.y -= settings.speed_x
    if event.key == pygame.K_DOWN and character1.rect.y + settings.speed_y * 2 <= settings.admin_height - (
            settings.admin_height * 0.19):
        character1.rect.y += settings.speed_x


def check_events(character1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, character1)


def update_screen(screen, character1):
    screen.fill((0, 0, 0))
    settings = Settings()
    pygame.draw.rect(screen, (6, 214, 103),
                     ((settings.width - settings.admin_width) // 2, 0,
                      settings.admin_width - (settings.width - settings.admin_width) // 2,
                      settings.admin_height - settings.admin_height * 0.19), 0)
    character1.blitme()
    pygame.display.flip()
