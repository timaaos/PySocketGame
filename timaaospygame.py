# Pygame шаблон - скелет для нового проекта Pygame
# !/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import ast
from threading import Timer
import random
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system, name
import pygame
import os

from utils import Block

screensize = [32, 16]

# Collect events until released

# import sleep to show output for some time period
from time import sleep


# define our clear function
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

        # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


import screen

receivequit = False
import keyboard


class player():
    def __init__(self):
        self.x = 0
        self.y = 0
        self.reload = False
        self.rotation = 0
        self.id = 0
        self.players = {}
        self.sockets = {}

    def move(self, x, y):
        self.x = x
        self.y = y
        movedict = {'event': 'move', 'x': self.x, 'y': self.y,
                    'id': str(myid)}
        # print(movedict)
        send(str(movedict))

    def infodict(self):
        return str({'x': self.x, 'y': self.y, 'id': myid})


def reload():
    sleep(1)
    player.reload = False
# Создаем игру и окно
pygame.init()
# настройка папки ассетов


WIDTH = 360
HEIGHT = 480
FPS = 30
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder, 'images')
player_img = pygame.image.load(os.path.join(img_folder, 'character_for_game.png')).convert()
pygame.quit()
class PlayerSpr(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = (0,0)
def reloadSprites():
    sprites = {}
    for key, value in player.players.items():
        newspr = PlayerSpr()
        newspr.x = value['x']
        newspr.y = value['y']
        print(newspr.x, newspr.y)
        sprites[value['id']] = newspr
        sprites[value['id']] = newspr


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            # print("i recieved: " + msg)
            if (msg == "{quit:true}"):
                receivequit = True
            # if("^sockets^" in msg):
            # player.sockets = ast.literal_eval(msg.split('⊘')[1])
            if ("^players^" in msg):
                send('getBlocks')
                player.players = ast.literal_eval(msg.split('⊘')[1])
                reloadSprites()
            if ("^blocks^" in msg):
                # print('igotblocks')
                player.blocks = ast.literal_eval(msg.split('⊘')[1])
            if (msg.startswith("^bullets^")):
                # print(msg.split(';')[0].split('R')[1][:-1])
                player.bullets = ast.literal_eval(msg.split(';')[0].split('R')[1])
            if ("{'event':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                # print(mydict)
                player.players[str(mydict['id'])]['x'] = mydict['x']
                player.players[str(mydict['id'])]['y'] = mydict['y']
                if(not str(mydict['id']) in sprites):
                    sprites[mydict['id']] = PlayerSpr()
                sprites[mydict['id']].rect.x = mydict['x']
                sprites[mydict['id']].rect.y = mydict['y']
            # if ("{'blockplace':" in msg):
            #    mydict = ast.literal_eval(msg.split(';')[0])
            #    player.blocks[str(mydict['block']['id'])] = mydict['block']
            #    player.renderPlayers()
            if ("updatePls" == msg):
                send("getPlayers")
            if ("giveInfo" == msg):
                send(player.infodict())
                send("getPlayers")

        except OSError:  # Possibly client has left the chat.
            break


def getplayerbyid(playerarr, id):
    for obj in playerarr:
        if obj.id == id:
            return obj
    return False


def send(msg):  # event is passed by binders.
    """Handles sending of messages."""
    # print("i sended: " + msg)
    msg = msg + ";"
    client_socket.send(bytes(msg, "utf8"))


# ----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
BUFSIZ = 32000
ADDR = (HOST, PORT)
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
player = player()
receive_thread = Thread(target=receive)
receive_thread.start()
player.id = str(random.randint(0, 9999))
send(str(player.id))
myid = player.id

pygame.init()
# настройка папки ассетов


WIDTH = 360
HEIGHT = 480
FPS = 30
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)







pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# Цикл игры
sprites = {}
for key, value in player.players.items():
    newspr = PlayerSpr()
    newspr.x = value['x']
    newspr.y = value['y']
    print(newspr.x, newspr.y)
    sprites[value['id']] = newspr

running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            #TODO: block placing
        elif event.type == pygame.KEYDOWN:
            xadd = 0
            yadd = 0
            print('keydown ' + str(event.key))
            if(event.key == pygame.K_w):
                yadd = -10
            if (event.key == pygame.K_s):
                yadd = 10
            if (event.key == pygame.K_d):
                xadd = 10
            if (event.key == pygame.K_a):
                xadd = -10
            player.move(player.x+xadd,player.y+yadd)

    # Обновление
    # Рендеринг
    screen.fill(BLACK)
    print(sprites)

    for key,value in sprites.items():
        screen.blit(value.image, (value.rect.x, value.rect.y))
    pygame.display.update()


pygame.quit()
