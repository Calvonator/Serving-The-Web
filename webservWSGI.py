import socket, io, sys

class WSGIServer(object):

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 1

    def __init__(self, server_address):
        #Create listen socket
        self.listen_socket = listen_socket = socket.socket(
            self.address_family,
            self.socket_type
        )
        #Allow address reuse
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #Bind the socket with address
        listen_socket.bind(server_address)

        #Activate
        listen_socket.listen(self.request_queue_size)

        #Get server hostname and port
        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port

        #Return headers set by Web framework/Web application
        self.headers_set = []

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        listen_socket = self.listen_socket
        while True:
            #New connection
            self.client_connection, client_address = listen_socket.accept()
            #Handle the request, close and wait for new request
            self.handle_one_request()

    def handle_one_request(self):
        request_data = self.client_connection.recv(1024)
        self.request_data = request_data = request_data.decode("utf-8")
        #Print request data formated with 'curl -v'
        print(''.join(
                f'< {line}\n' for line in request_data.splitlines()
            )
        )
        
        self.parse_request(request_data)

        #Create environment dictionary using request data
        env = self.get_environment()

        #Here we call out application callable and get back a result that will become the HTTP responce body
        result = self.application(env, self.start_response)

        #Construct a response and send it back to the client
        self.finish_response(result)

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        request_line = request_line.rstrip('\r\n')
        #Break down the request line into components
        (self.request_method,   #GET
        self.path,              #/hello
        self.request_version    #HTTP/1.1
        ) = request_line.split()

    def get_environment(self):
        env = {}
        # The following code snippet does not follow PEP8 conventions
        # but it's formatted the way it is for demonstration purposes
        # to emphasize the required variables and their values
        #
        # Required WSGI variables

        env['wsgi.verson'] = (1,0)
        env['wsgi.url_scheme'] = 'http'
        env['wsgi.input'] = io.StringIO(self.request_data)
        env['wsgi.errors'] = sys.stderr
        env['wsgi.multithread'] = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once'] = False
        
        # Required CGI Variables
        env['REQUEST_METHOD'] = self.request_method     # GET
        env['PATH_INFO'] = self.path                    # /hello
        env['SERVER_NAME'] = self.server_name           # localhost
        env['SERVER_POST'] = str(self.server_port)      # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):
        # Add necessary headers
        server_headers = [
            ('Date', 'Mon, 31 Aug 2020 2:00 PM AWST'),
            ('Server', 'WSGIServer 0.2')
        ]
        self.headers_set = [status, response_headers + server_headers]
        # To adhere to WSGI specification the start_response must return
        # a 'write' callable. We simplicity's sake we'll ignore that detail
        # for now.
        # return self.finish_response

    def finish_response(self, result):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 P{status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            
            response += '\r\n'

            for data in result:
                response += data.decode('utf-8')
            # Print formatted response data 
            print(''.join(
                    f'> {line}\n' for line in response.splitlines()
                )
            )
            response_bytes = response.encode()
            self.client_connection.sendall(response_bytes)
        finally:
            self.client_connection.close()

SERVER_ADDRESS = (HOST, PORT) = '', 8888

def make_server(server_address, application):
    server= WSGIServer(server_address)
    server.set_app(application)
    return server

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    moudle, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
    httpd.serve_forever()

