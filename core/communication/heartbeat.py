import socket
import json
import sys
from core.databaseRedis import nodesDB as db


def getRes(HOST):
    PORT = 9999
    data = "heartbeat"

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        
        # Connect to server and send data
        print("attempt connection to " + HOST)
        sock = socket.create_connection((HOST, PORT), timeout= 1)
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
        recJson = json.loads(received)
        cpu = recJson["cpu"]
        memory = recJson["memory"]

        print "Memory {} MB".format(memory / 1048576)
        print "CPU {} %".format(cpu)

        # update record in DB

    except socket.timeout:
        print("disconnected " + HOST)
        recJson = None
    finally:
        sock.close()

    return recJson


def sendAll():
    nodes = db.getNodesIP()

    for n in nodes:
        res = getRes(n.ip)
        if(res):
            db.updateResources(n.id, res)
        else:
            db.deleteNode(n.id)

if __name__ == '__main__':
    getRes(sys.argv[0])
