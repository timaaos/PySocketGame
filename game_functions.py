import pygame
import sys
from settings import Settings
from block import Block

block_list = []


def check_down_events(event, character1):
    settings = Settings()
    if event.key == pygame.K_RIGHT and character1.rect.x + settings.speed_x * 2 < settings.width - (
            settings.width - settings.admin_width) // 2:
        character1.x += settings.speed_x
        character1.centerx += settings.speed_x
    if event.key == pygame.K_LEFT and character1.rect.x - settings.speed_x >= (
            settings.width - settings.admin_width) // 2:
        character1.x -= settings.speed_x
        character1.centerx -= settings.speed_x
    if event.key == pygame.K_UP and character1.rect.y - settings.speed_y >= 0:
        character1.y -= settings.speed_y
        character1.centery -= settings.speed_y
    if event.key == pygame.K_DOWN and character1.rect.y + settings.speed_y * 2 <= settings.admin_height - (
            settings.admin_height * 0.20):
        character1.y += settings.speed_y
        character1.centery += settings.speed_y


def check_mouse_events(event):
    settings = Settings()
    block_list.append([event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y])


def check_events(screen, character1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, character1)
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_events(event)


def update_screen(screen, character1):
    screen.fill((0, 0, 0))
    settings = Settings()
    pygame.draw.rect(screen, (6, 214, 103),
                     ((settings.width - settings.admin_width) // 2, 0,
                      settings.admin_width - (settings.width - settings.admin_width) // 4,
                      settings.admin_height - settings.admin_height * 0.20), 0)
    character1.blitme()
    for i in block_list:
        Block(screen, i[0], i[1]).blitme()
    pygame.display.flip()
