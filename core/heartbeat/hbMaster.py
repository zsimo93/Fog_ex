import socket
import json
from time import sleep
from threading import Thread
from core.databaseMongo import nodesDB as db


def getRes(id, IP):
    PORT = 9999
    data = "heartbeat"

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock = socket.create_connection((IP, PORT), timeout=1)
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
        recJson = json.loads(received)

    except Exception:
        recJson = None
        memory = db.getRes(id)["memory"]
        if memory < 0:
            return
    finally:
        sock.close()

    if recJson:
        db.updateResources(id, recJson)
    else:
        db.deleteNode(id)
    return


def sendAll():
    nodes = db.getNodesIP()

    for n in nodes:
        Thread(target=getRes, args=(n.id, n.ip, )).start()

def start():
    while(True):
        sleep(0.5)
        sendAll()
