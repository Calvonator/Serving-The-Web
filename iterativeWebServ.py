import socket, mysql.connector, pickle, threading

SERVER_ADDRESS = (HOST, PORT) = '', 8886
REQUEST_QUEUE_SIZE = 5

logged = 0



class login_object:
    username = ""
    password = ""

def handle_request(client_connection):
    request = client_connection.recv(1024)
    request = request.decode()
    flag = request[0:3]
    clientNum = request[3]
    print("Flag: " + flag)

    if flag == "f01":
        print("Incoming message from client #" + str(clientNum))

    print(request)
    http_response = b"""
HTTP/1.1 200 OK

Hello, World!
"""
    client_connection.sendall(http_response)

def authentication_handler(client_sock):
    print("Authenticating Client")
    login_request = client_sock.recv(1024)

    login_data = pickle.loads(login_request)    
    
    print(login_data.username)
    print(login_data.password)

    logged + 1

    #print(login_request.decode())


    print("Authentication completed; closing connection")
    client_sock.close()




def serve_forever():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind(SERVER_ADDRESS)
    listen_socket.listen(REQUEST_QUEUE_SIZE)
    print('Serving HTTP on port {port} ... \n'.format(port=PORT))

    auth_threads = []

    while True:
        print(logged)        
        client_connection, client_address = listen_socket.accept()
        thread = threading.Thread(target=authentication_handler, args=(client_connection,))
        auth_threads.append(thread)
        thread.start()
        #authentication_handler(client_connection)
        #client_connection.close()



if __name__ == "__main__":
    serve_forever() 