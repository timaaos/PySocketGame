import pygame
import sys
from settings import Settings
from block import Block

block_list = []
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)

def check_down_events(event, character1):
    settings = Settings()
    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and character1.x + settings.speed_x * 2 < settings.width - (
            settings.width - settings.admin_width) // 2:
        character1.x += settings.speed_x
        character1.centerx += settings.speed_x
    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and character1.x - settings.speed_x >= (
            settings.width - settings.admin_width) // 2:
        character1.x -= settings.speed_x
        character1.centerx -= settings.speed_x
    if (event.key == pygame.K_UP or event.key == pygame.K_w) and character1.y - settings.speed_y >= 0:
        character1.y -= settings.speed_y
        character1.centery -= settings.speed_y
    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and character1.y + settings.speed_y * 2 <= settings.admin_height - (
            settings.admin_height * 0.20):
        character1.y += settings.speed_y
        character1.centery += settings.speed_y


def check_mouse_events(event):
    settings = Settings()
    if pygame.mouse.get_pressed()[2]:
        block_list.append([event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y])
    if pygame.mouse.get_pressed()[0]:
        print("lmb clicked")
        #TODO: block destroy


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
    textsurface = myfont.render('Arrows, WASD - Moving', False, (255, 255,255))
    textsurface2 = myfont.render('Right Click - Place Block', False, (255, 255, 255))
    textsurface3 = myfont.render('Left Click - Destroy Block', False, (255, 255, 255))
    character1.blitme()
    screen.blit(textsurface, (200, 0))
    screen.blit(textsurface2, (200, 50))
    screen.blit(textsurface3, (200, 100))
    for i in block_list:
        Block(screen, i[0], i[1]).blitme()
    pygame.display.flip()
