#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Server for multithreaded (asynchronous) chat application."""
import time
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ast



def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("{connected:true}", "utf8"))
        broadcast(bytes('updatePls','utf8'))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

def infolog(msg):
    print('[INFO]: ' + msg)
def eventlog(msg):
    print('[EVENT]: ' + msg)

def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")[:-1]
    client.send(bytes('giveInfo', 'utf8'))
    clients[client] = name
    clientsbyname[name] = client
    player_list[name] = ast.literal_eval(client.recv(BUFSIZ).decode("utf8")[:-1])
    infolog('Player with id ' + name + ' joined')
    broadcast(bytes("^players^⊘" + str(player_list), 'utf8'))
    while True:
        msg = client.recv(BUFSIZ)
        if msg == bytes("getPlayers", "utf8"):
            infolog('Replied to getPlayers command by ' + name)
            client.send(bytes("^players^⊘" + str(player_list), 'utf8'))
        if 'getBlocks' in msg.decode('utf8'):
            infolog('Replied to getBlocks command by ' + name)
            client.send(bytes("^blocks^⊘" + str(block_list), 'utf8'))
        if ("{'event':" in msg.decode('utf8')):
            mydict = ast.literal_eval(msg.decode('utf8').split(';')[0])
            player_list[str(mydict['id'])]['x_pos'] = mydict['x_pos']
            player_list[str(mydict['id'])]['y_pos'] = mydict['y_pos']
            broadcast(msg)
            eventlog('MoveEvent event by ' + name + ' to x:' + str(mydict['x_pos']) + ' y:' + str(mydict['y_pos']))
        if ("{'blockplace':" in msg.decode('utf8')):
            mydict = ast.literal_eval(msg.decode('utf8').split(';')[0])
            block_list.append(
                [mydict['x_pos'], mydict['y_pos']])
            broadcast(msg)
            eventlog('BlockPlace event by ' + name)
        if ("{'blockremove':" in msg.decode('utf8')):
            mydict = ast.literal_eval(msg.decode('utf8').split(';')[0])
            block_list.remove([mydict['x_pos'],mydict['y_pos']])
            broadcast(msg)
            eventlog('BlockRemove event by ' + name)
        if('closeMe' in msg.decode('utf8')):
            infolog(name + ' leaved!')
            break
    del clients[client]
    del clientsbyname[name]
    del player_list[name]


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)

clients = {}
clientsbyname = {}
addresses = {}
player_list = {}
block_list = []
bullets = {}

HOST = ''
PORT = 33000
BUFSIZ = 32000
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)
if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
