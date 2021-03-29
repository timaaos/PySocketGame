import pygame
import sys
from settings import Settings
from block import Block
import inputbox

block_list = []
pygame.font.init()  # you have to call this at the start,
# if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 20)


def check_down_events(event, character1, screen):
    settings = Settings()
    if (event.key == pygame.K_t):
        command = inputbox.ask(screen, "Enter command(help for help)")
        if command == ['h', 'e', 'l', 'p']:
            inputbox.say(screen, "teleport/tp - teleports player, using: tp 10 10", 0, True)
        elif "".join(command).startswith("tp") or "".join(command).startswith("teleport"):
            args = "".join(command).split(" ")
            if(not len(args) == 3):
                inputbox.say(screen,"Oops! Wrong usage!",0,True)
                return
            character1.x = (int(args[1]) - 1) * settings.speed_x
            character1.y = (int(args[2]) - 1) * settings.speed_y
        else:
            inputbox.say(screen,"Oops! This command doesnt exists!",0,True)
            return
    if (
            event.key == pygame.K_RIGHT or event.key == pygame.K_d) and character1.x + settings.speed_x * 2 < settings.width - (
            settings.width - settings.admin_width) // 2 and not isBlock(character1.x + settings.speed_x, character1.y):
        character1.x += settings.speed_x
        character1.centerx += settings.speed_x
    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and character1.x - settings.speed_x >= (
            settings.width - settings.admin_width) // 2 and not isBlock(character1.x - settings.speed_x, character1.y):
        character1.x -= settings.speed_x
        character1.centerx -= settings.speed_x
    if (event.key == pygame.K_UP or event.key == pygame.K_w) and character1.y - settings.speed_y >= 0 and not isBlock(
            character1.x, character1.y - settings.speed_y):
        character1.y -= settings.speed_y
        character1.centery -= settings.speed_y
    if (
            event.key == pygame.K_DOWN or event.key == pygame.K_s) and character1.y + settings.speed_y * 2 <= settings.admin_height - (
            settings.admin_height * 0.20) and not isBlock(character1.x, character1.y + settings.speed_y):
        character1.y += settings.speed_y
        character1.centery += settings.speed_y


def isBlock(x, y):
    for block in block_list:
        if block[0] == x and block[1] == y:
            return True
    return False


def check_mouse_events(event):
    settings = Settings()
    if pygame.mouse.get_pressed()[2]:
        if ((event.pos[1] - event.pos[
            1] % settings.speed_y) + settings.speed_y < settings.admin_height - settings.admin_height * 0.20):
            block_list.append(
                [event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y])
    if pygame.mouse.get_pressed()[0]:
        print("lmb clicked")
        # TODO: block destroy


def check_events(screen, character1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, character1, screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_events(event)


def update_screen(screen, character1):
    screen.fill((0, 0, 0))
    settings = Settings()
    pygame.draw.rect(screen, (6, 214, 103),
                     ((settings.width - settings.admin_width) // 2, 0,
                      settings.admin_width - (settings.width - settings.admin_width) // 4,
                      settings.admin_height - settings.admin_height * 0.20), 0)
    textsurface = myfont.render('Arrows, WASD - Moving', False, (255, 255, 255))
    textsurface2 = myfont.render('Right Click - Place Block', False, (255, 255, 255))
    textsurface3 = myfont.render('Left Click - Destroy Block', False, (255, 255, 255))
    textsurface4 = myfont.render('T - Open console', False, (255, 255, 255))
    character1.blitme()
    screen.blit(textsurface, (0, 700))
    screen.blit(textsurface2, (0, 733))
    screen.blit(textsurface3, (0, 766))
    screen.blit(textsurface4, (250, 700))
    for i in block_list:
        Block(screen, i[0], i[1]).blitme()
    pygame.display.flip()
