import SocketServer
import psutil
import json

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()

        cpu = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory().available

        response = {
            'cpu': cpu,
            'memory': memory
        }

        self.request.sendall(json.dumps(response))

def start():
    HOST, PORT = "localhost", 9999
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()