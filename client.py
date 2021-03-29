#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import ast
from threading import Timer
import random
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system, name
from enum import Enum
from termcolor2 import colored
from termcolor import cprint
import colorama

from utils import Block, Bullet

colorama.init()


class Rotation(Enum):
    UP = 0
    DOWN = 2
    LEFT = 3
    RIGHT = 1


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
        self.char = rotationchar[0]
        self.rotation = 0
        self.id = 0
        self.players = {}
        self.sockets = {}
        self.blocks = {}
        self.bullets = {}
        self.delays = False

    def move(self, forward, rotation=0):
        if not self.delays:

            xadd = 0
            yadd = 0
            if (rotation == 1):
                self.rotation += 1
            if (rotation == -1):
                self.rotation -= 1
            if (self.rotation == 0):
                yadd = -1
            if (self.rotation == 1):
                xadd = 1
            if (self.rotation == 2):
                yadd = 1
            if (self.rotation == 3):
                xadd = -1
            if (self.rotation > 3):
                self.rotation = 0
            if (self.rotation < 0):
                self.rotation = 3
            if (not self.isBlock(self.getBackwardPos()) and forward < 0):
                self.x -= xadd
                self.y -= yadd
            if (not self.isBlock(self.getForwardPos()) and forward > 0):
                self.x += xadd
                self.y += yadd
            if (self.x > screensize[0] - 1):
                self.x = 0
            elif (self.x < 0):
                self.x = screensize[0] - 1
            if (self.y > screensize[1] - 1):
                self.y = 0
            elif (self.y < 0):
                self.y = screensize[1] - 1
            self.char = rotationchar[self.rotation]
            send(str(movedict))
            self.delays = True
            sleep(0.15)
            self.delays = False
        else:
            return

    def getForwardPos(self):
        yadd = 0
        xadd = 0
        if (self.rotation == 0):
            yadd = -1
        if (self.rotation == 1):
            xadd = 1
        if (self.rotation == 2):
            yadd = 1
        if (self.rotation == 3):
            xadd = -1
        x = self.x + xadd
        y = self.y + yadd
        return (x, y)

    def getBackwardPos(self):
        yadd = 0
        xadd = 0
        if (self.rotation == 0):
            yadd = 1
        if (self.rotation == 1):
            xadd = -1
        if (self.rotation == 2):
            yadd = -1
        if (self.rotation == 3):
            xadd = 1
        x = self.x + xadd
        y = self.y + yadd
        return (x, y)

    def Tips(self):
        print('X:' + str(player.x))
        print('Y:' + str(player.y))
        print("Controls:\nWAD - Move, Rotate\nE - Place Block\nESC - Leave")

    def placeBlock(self):
        block = Block('clay')
        block.x = player.getForwardPos()[0]
        block.y = player.getForwardPos()[1]
        if (not self.isBlock(player.getForwardPos())):
            send(str({'blockplace': True, 'block': block.getInfo()}))

    def isBlock(self, pos):
        for key, value in player.blocks.items():
            if (value['x'] == pos[0] and value['y'] == pos[1]):
                return True
        return False
    def pewpew(self):
        if (self.reload): return
        bullet = Bullet()
        bullet.x = self.getForwardPos()[0]
        bullet.y = self.getForwardPos()[1]
        xadd = 0
        yadd = 0
        if (self.rotation == 0):
            yadd = -1
        if (self.rotation == 1):
            xadd = 1
        if (self.rotation == 2):
            yadd = 1
        if (self.rotation == 3):
            xadd = -1
        bullet.xadd = xadd
        bullet.yadd = yadd
        send(str({'bulletmove': True, 'bullet': bullet.getInfo()}))
        reload()

    def infodict(self):
        return str({'x': self.x, 'y': self.y, 'char': player.char, 'id': player.id})

    def renderPlayers(self):
        clear()
        screenobj = screen.screen(screensize[0], screensize[1])
        for key, value in self.players.items():
            screenobj.changePx(value['char'], value['x'], value['y'])
        for key, value in self.blocks.items():
            screenobj.changePx(value['char'], value['x'], value['y'])
        for key, value in self.bullets.items():
            screenobj.changePx(screen.Blocks.BULLET.value, value['x'], value['y'])
        print(screenobj.screenstr)
        self.Tips()


def reload():
    sleep(1)
    player.reload = False


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
                player.renderPlayers()
            if ("^blocks^" in msg):
                # print('igotblocks')
                player.blocks = ast.literal_eval(msg.split('⊘')[1])
                player.renderPlayers()
            if (msg.startswith("^bullets^")):
                # print(msg.split(';')[0].split('R')[1][:-1])
                player.bullets = ast.literal_eval(msg.split(';')[0].split('R')[1])
                player.renderPlayers()
            if ("{'event':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                # print(mydict)
                player.players[str(mydict['id'])]['x'] = mydict['x']
                player.players[str(mydict['id'])]['y'] = mydict['y']
                player.players[str(mydict['id'])]['char'] = mydict['char']
                player.players[str(mydict['id'])]['rotation'] = mydict['rotation']
                player.renderPlayers()
            if ("{'blockplace':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                player.blocks[str(mydict['block']['id'])] = mydict['block']
                player.renderPlayers()
            if ("{'bulletmove':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                # print(mydict)
                player.bullets[str(mydict['bullet']['id'])] = mydict['bullet']
            if ("{update}" == msg):
                send("getPlayers")
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
BUFSIZ = 2048
ADDR = (HOST, PORT)
print("Colors:")
cprint('Blue 1', 'blue', 'on_grey')
cprint('Red 2', 'red', 'on_grey')
cprint('Cyan 3', 'cyan', 'on_grey')
cprint('Magenta 4', 'magenta', 'on_grey')
colornum = input("Enter color:")
if (colornum == '1'):
    color = 'blue'
elif (colornum == '2'):
    color = 'red'
elif (colornum == '3'):
    color = 'cyan'
elif (colornum == '4'):
    color = 'magenta'
rotationchar = [colored('↑', 'white', 'on_' + color), colored('→', 'white', 'on_' + color),
                colored('↓', 'white', 'on_' + color), colored('←', 'white', 'on_' + color)]
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
player = player()
receive_thread = Thread(target=receive)
receive_thread.start()
player.id = str(random.randint(0, 9999))
send(str(player.id))
