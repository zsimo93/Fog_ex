import socket
import json
import sys

def heartbeat(HOST):
    PORT = 9999
    data = "heartbeat"

    # Create a socket (SOCK_STREAM means a TCP socket)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to server and send data
        sock.connect((HOST, PORT))
        sock.sendall(data + "\n")

        # Receive data from the server and shut down
        received = sock.recv(1024)
        recJson = json.loads(received)
        cpu = recJson["cpu"]
        memory = recJson["memory"]

        print "Memory {} MB".format(memory/1048576) 
        print "CPU {} %".format(cpu)

        # update record in DB

    except Exception:
        # handle disconnection
        print ("disconnected")

    finally:
        print ("closing socket")
        sock.close()

heartbeat(sys.argv[0])