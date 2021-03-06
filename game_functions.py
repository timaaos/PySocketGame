import pygame
import sys

from character import Character
from settings import Settings
from block import Block
import inputbox

block_list = []
player_list = {}
character_list = {}
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
        character1.move = True
    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and character1.x - settings.speed_x >= (
            settings.width - settings.admin_width) // 2 and not isBlock(character1.x - settings.speed_x, character1.y):
        character1.x -= settings.speed_x
        character1.centerx -= settings.speed_x
        character1.move = True
    if (event.key == pygame.K_UP or event.key == pygame.K_w) and character1.y - settings.speed_y >= 0 and not isBlock(
            character1.x, character1.y - settings.speed_y):
        character1.y -= settings.speed_y
        character1.centery -= settings.speed_y
        character1.move = True
    if (
            event.key == pygame.K_DOWN or event.key == pygame.K_s) and character1.y + settings.speed_y * 2 <= settings.admin_height - (
            settings.admin_height * 0.20) and not isBlock(character1.x, character1.y + settings.speed_y):
        character1.y += settings.speed_y
        character1.centery += settings.speed_y
        character1.move = True


def isBlock(x, y):
    for block in block_list:
        if block[0] == x and block[1] == y:
            return True
    return False
def isPlayer(x, y):
    for k,v in player_list.items():
        if v['x_pos'] == x and v['y_pos'] == y:
            return True
    return False
def delBlock(x,y):
    for block in block_list:
        if block[0] == x and block[1] == y:
            del block_list[block_list.index(block)]

def check_mouse_events(event,character1):
    settings = Settings()
    if pygame.mouse.get_pressed()[2]:
        if ((event.pos[1] - event.pos[
            1] % settings.speed_y) + settings.speed_y < settings.admin_height - settings.admin_height * 0.20 and not isBlock(event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y) and not isPlayer(event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y)):
            #block_list.append(
            #    [event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y])
            character1.setblockvar = True
            character1.setblockpos = (event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y)
    if pygame.mouse.get_pressed()[0]:
        if(isBlock(event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y)):
            #delBlock(event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y)
            character1.remblockvar = True
            character1.remblockpos = (event.pos[0] - event.pos[0] % settings.speed_x, event.pos[1] - event.pos[1] % settings.speed_y)


def check_events(screen, character1):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
            #pygame.quit()
            #sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_down_events(event, character1, screen)
        if event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_events(event,character1)
    return True

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
    screen.blit(textsurface, (0, 700))
    screen.blit(textsurface2, (0, 733))
    screen.blit(textsurface3, (0, 766))
    screen.blit(textsurface4, (250, 700))
    for i in block_list:
        pygame.draw.rect(screen,(155, 155, 155),(i[0],i[1],settings.speed_x,settings.speed_y))
        pygame.draw.rect(screen, (55, 55, 55), (i[0]-5, i[1]-5, settings.speed_x, settings.speed_y),10)
        #Block(screen, i[0], i[1]).blitme()

    for k,v in player_list.items():
        Character(screen,v['x_pos'],v['y_pos']).blitme()
    for k, v in player_list.items():
        textname = myfont.render(v['name'], False, (255, 255, 255))
        screen.blit(textname, (v['x_pos'], v['y_pos']-33))
    pygame.display.flip()
