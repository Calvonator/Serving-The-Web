import socket, pickle


SERVER_ADDRESS = (HOST, PORT) = '127.0.0.1', 8888


class login_object:
    username = ""
    password = ""


class client_silly(object):


    def __init__(self, name, RHOST, PORT):
        self.RHOST = RHOST
        self.PORT = PORT
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = name

    def login(self):
        print("Please provide account details...")
        uname = input("Username:\n")
        pword = input("Password:\n")
        newLogin = login_object()
        newLogin.username = uname
        newLogin.password = pword
        
        login_request = pickle.dumps(newLogin)
        
        print("Connecting..")
        self.connect()
        print("Connected... Sending login data")
        self.sock.sendall(login_request)
        self.sock.close()
        print("Closing Connection")



    def connect(self):
        self.sock.connect((self.RHOST, self.PORT))

    def send_msg(self):                             #Self-contained socket, will cause Pipe error if this function is run while the object is connected using connect fucntion
        msg = "f01"
        msg += client.name
        msg += input("What is your messsage?")
        msg += "\n"
        self.connect()
        self.sock.sendall(msg.encode())
        self.disconnect()

    def disconnect(self):
        close_response = 'Client ' + self.name + ' disconnecting...'
        self.sock.sendall(close_response.encode())
        self.sock.close()

client = client_silly('1', '192.168.80.132', 8888)

client.login()
