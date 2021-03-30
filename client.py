#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import ast
import random
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from os import system, name
from termcolor2 import colored
from termcolor import cprint
from time import sleep

def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if ("^players^" in msg):
                send('getBlocks')
                player.players = ast.literal_eval(msg.split('⊘')[1])
            if ("^blocks^" in msg):
                player.blocks = ast.literal_eval(msg.split('⊘')[1])
            if ("{'event':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                player.players[str(mydict['id'])]['x'] = mydict['x']
                player.players[str(mydict['id'])]['y'] = mydict['y']
                player.players[str(mydict['id'])]['char'] = mydict['char']
                player.players[str(mydict['id'])]['rotation'] = mydict['rotation']
            if ("{'blockplace':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                player.blocks[str(mydict['block']['id'])] = mydict['block']
            if ("{update}" == msg):
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
receive_thread = Thread(target=receive)
receive_thread.start()
player.id = str(random.randint(0, 9999))
send(str(player.id))
