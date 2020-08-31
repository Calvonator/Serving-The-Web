import socket

HOST, PORT = "", 8888

#Create the socket using AF_INET address family (IPV4)
listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Set the options for the socket 
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#Bind the set address and port to the socket. Empty host becomes localhost
listen_socket.bind((HOST, PORT))
#The socket now listents for incoming requests so that accept() can receive the requests
listen_socket.listen(1)
print(f'Serving HTTP File on {PORT} ... ')
while True:
    #This line here waits until a request is handed to accept() by the listen socket. A new socket is created for the connection in client_connection
    client_connection, client_address = listen_socket.accept()
    #Once a connection comes through, the data is received and placed into request_data in byte form
    request_data = client_connection.recv(1024)
    #The request data is then decoded in "utf-8" formatand printed to console.
    print(request_data.decode("utf-8"))


    http_response = b"""
HTTP/1.1 200 OK

Hello, World!
"""
    #The bytes in http_response are sent back over the client connection socket and then the socket is closed.
    client_connection.sendall(http_response)
    client_connection.close()

    #New connections will now be accepted.
