#!/usr/bin/env python3
"""Server for multithreaded (asynchronous) chat application."""
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import ast

global getPlayerDict

getPlayerDict = {}


def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("{connected:true}", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()


def handle_client(client):  # Takes client socket as argument.
    """Handles a single client connection."""

    name = client.recv(BUFSIZ).decode("utf8")[:-1]
    client.send(bytes('giveInfo', 'utf8'))

    clients[client] = name
    clientsbyname[name] = client
    players[name] = ast.literal_eval(client.recv(BUFSIZ).decode("utf8")[:-1])
    print(clients)
    broadcast(bytes("^players^⊘" + str(players), 'utf8'))
    while True:
        msg = client.recv(BUFSIZ)
        print(msg.decode('utf8'))
        if msg == bytes("{quit:true}", "utf8"):
            client.send(bytes("{quit:true}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("{msg:'%s has left the game.'}" % name, "utf8"))
            break
        if msg == bytes("getPlayers", "utf8"):
            client.send(bytes("^players^⊘" + str(players), 'utf8'))
        if ("{'event':" in msg.decode('utf8')):
            mydict = ast.literal_eval(msg.decode('utf8').split(';')[0])
            print(mydict)
            players[str(mydict['id'])]['x'] = mydict['x']
            players[str(mydict['id'])]['y'] = mydict['y']
            players[str(mydict['id'])]['char'] = mydict['char']

            broadcast(bytes(msg.decode('utf8').split(';')[0], 'utf8'))
        if ("{'blockplace':" in msg.decode('utf8')):
            mydict = ast.literal_eval(msg.decode('utf8').split(';')[0])
            print(mydict)
            blocks[str(mydict['block']['id'])] = mydict['block']
            broadcast(bytes(msg.decode('utf8').split(';')[0], 'utf8'))

    del clients[client]
    del clientsbyname[name]
    del players[name]


def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8") + msg)


clients = {}
clientsbyname = {}
addresses = {}
players = {}
blocks = {}

HOST = ''
PORT = 33000
BUFSIZ = 1024
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
