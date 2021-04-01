import sys
import time

import pygame

import game_functions
import inputbox
from settings import Settings
from game_functions import check_events, update_screen, block_list, delBlock, character_list, player_list
from character import Character
import random
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ast
def stoppls():
    send('closeMe')
    client_socket.close()
    pygame.quit()
    sys.exit()


def receive():
    """Handles receiving of messages."""
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            if ("^players^" in msg):
                send('getBlocks')
                game_functions.player_list = ast.literal_eval(msg.split('⊘')[1])
            if ("^blocks^" in msg):
                game_functions.block_list = ast.literal_eval(msg.split('⊘')[1])
            if ("{'event':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                game_functions.player_list[str(mydict['id'])]['x_pos'] = mydict['x_pos']
                game_functions.player_list[str(mydict['id'])]['y_pos'] = mydict['y_pos']
            if ("{'blockplace':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                game_functions.block_list.append(
                    [mydict['x_pos'],mydict['y_pos']])
            if ("{'blockremove':" in msg):
                mydict = ast.literal_eval(msg.split(';')[0])
                game_functions.block_list.remove([mydict['x_pos'],mydict['y_pos']])
            if ("{update}" == msg):
                send("getPlayers")
            if("giveInfo" == msg):
                send(character.sendMyData())
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
if __name__ == '__main__':
    """Создаем окно в pygame"""
    pygame.init()
    settings = Settings()
    size = width, height = settings.width, settings.height - 50
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    """Главный игровой цикл"""
    clock = pygame.time.Clock()
    pos = x, y = (settings.width - settings.admin_width) // 2, 0
    character = Character(screen, x, y)
    """Серверная часть"""
    HOST = "".join(inputbox.ask(screen,'Enter host'))
    PORT = "".join(inputbox.ask(screen,'Enter port'))
    character.name = "".join(inputbox.ask(screen, 'Enter nickname'))
    if not PORT:
        PORT = 33000
    else:
        PORT = int(PORT)
    BUFSIZ = 4096
    ADDR = (HOST, PORT)
    client_socket = socket(AF_INET, SOCK_STREAM)
    client_socket.connect(ADDR)
    receive_thread = Thread(target=receive)
    receive_thread.start()
    character.id = str(random.randint(0, 9999))
    send(str(character.id) + "♣" + str(character.name))

    close = True
    """Конец серверной части"""
    while close:
        close = check_events(screen, character)
        character.update()
        if(character.move):
            send(character.sendMoveData())
        if (character.setblockvar):
            send(character.setBlock())
        if (character.remblockvar):
            send(character.remBlock())
        # Рисуем поле
        update_screen(screen, character)
        clock.tick(settings.fps)
    stoppls()
#!/usr/bin/env python3
"""Script for Tkinter GUI chat client."""
import ast



# ----Now comes the sockets part----
