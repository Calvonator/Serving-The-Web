import socket
from time import sleep

class client_silly(object):


    def __init__(self, name, RHOST, PORT):
        self.RHOST = RHOST
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name
        self.connect()
        self.annoy_the_server(5)

    
    def connect(self):
        self.sock.connect((self.RHOST, self.PORT))

    def send_response(self, msg):
        #msg = input("What message would you like to send?")
        self.sock.sendall(msg.encode())

    def disconnect(self):
        close_response = 'Client ' + self.name + ' disconnecting...'
        self.sock.sendall(close_response.encode())
        self.sock.close()

    def annoy_the_server(self, iterations):
        for x in range(iterations):
            annoy_response = "Client " + self.name + ": Annoyance #" + str(x) + '\n' 
            self.sock.sendall(annoy_response.encode('utf-8'))


client = client_silly('1', '127.0.0.1', 8888)

#client.connect()
client.send_response("hello lolsald")
#client.annoy_the_server(5)
client.disconnect()

#clients = [client_silly(str(x), '127.0.0.1', 8888) for x in range(5)]

#ctr = 1

#for client_socket in clients:

    #client_socket.connect(('127.0.0.1', 8888))

    #connecting_announce = 'Client ' + str(ctr) + ' connecting'

    #client_socket.sendall(connecting_announce.encode('utf-8'))

    #client_socket.connect()

    #client_socket.annoy_the_server(5)

    #client_socket.disconnect()

    #connect_response = client_socket.recv(1024)

    #print(connect_response.decode())

    #ctr += 1