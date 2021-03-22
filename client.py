#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import ast
import random
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system, name
screensize = [32,16]

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
        self.char = screen.randomPlayer()
        self.id = 0
        self.players = {}
        self.sockets = {}
        self.delays = False
    def move(self, xadd, yadd):
        if not self.delays:
            self.x += xadd
            self.y += yadd
            if (self.x > screensize[0]-1):
                self.x = 0
            elif(self.x < 0):
                self.x = screensize[0]-1
            if (self.y > screensize[1]-1):
                self.y = 0
            elif(self.y < 0):
                self.y = screensize[1]-1
            movedict = {'event': 'move', 'x': self.x, 'y': self.y, 'id': str(self.id)}
            print(movedict)
            send(str(movedict))
            self.delays = True
            sleep(0.05)
            self.delays = False
    def debugInfo(self):
        print('X:' + str(player.x))
        print('Y:' + str(player.y))
        print('char:' + str(player.char))
        print('id:' + str(player.id))
        print('Players:' + str(player.players))
    def infodict(self):
        return str({'x':self.x,'y':self.y,'char':player.char,'id':player.id})
    def renderPlayers(self):
        clear()
        screenobj = screen.screen(screensize[0], screensize[1])
        for key, value in self.players.items():
            screenobj.changePx(value['char'], value['x'], value['y'])
        print(screenobj.screenstr)
        self.debugInfo()


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            print("i recieved: " + msg)
            if (msg == "{quit:true}"):
                receivequit = True
            #if("^sockets^" in msg):
                #player.sockets = ast.literal_eval(msg.split('⊘')[1])
            if("^players^" in msg):
                player.players = ast.literal_eval(msg.split('⊘')[1])
                player.renderPlayers()
            if ("{'event':" in msg):
                mydict = ast.literal_eval(msg)
                print(mydict)
                player.players[str(mydict['id'])]['x'] = mydict['x']
                player.players[str(mydict['id'])]['y'] = mydict['y']
                player.renderPlayers()
            if ("{update}" == msg):
                send("getPlayers")
            if("giveInfo" == msg):
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
    print("i sended: " + msg)
    client_socket.send(bytes(msg, "utf8"))


# ----Now comes the sockets part----
HOST = input('Enter host: ')
PORT = input('Enter port: ')
if not PORT:
    PORT = 33000
else:
    PORT = int(PORT)
BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)
player = player()
receive_thread = Thread(target=receive)
receive_thread.start()
player.id = str(random.randint(0, 9999))
send(str(player.id))
keyboard.on_press_key("w", lambda _:player.move(0,-1))
keyboard.on_press_key("a", lambda _:player.move(-1,0))
keyboard.on_press_key("s", lambda _:player.move(0,1))
keyboard.on_press_key("d", lambda _:player.move(1,0))
keyboard.on_press_key("e", lambda _:player.debugInfo())
keyboard.on_press_key("esc", lambda _:exit())