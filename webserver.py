import socket
from httprequestprocessor import HttpRequestProcessor


class Webserver:
    def __init__(self, server_ip, server_port, queue_size, static_folder_loc):
        self.ip = server_ip
        self.port = server_port
        self.queue = queue_size
        self.folder = static_folder_loc
        self.handlers = {}

    def add_handler(self, handler_function, http_verb, address):
        self.handlers[http_verb + address] = handler_function

    def run(self):
        # create an INET, STREAMing socket
        serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serversocket.bind((self.ip, self.port))
        # become a server socket
        serversocket.listen(self.queue)

        while True:
            conn, addr = serversocket.accept()
            httpreq = HttpRequestProcessor()
            with conn:
                print('Connected by', addr)
                while httpreq.keep_receiving():
                    data = conn.recv(1024)
                    if not data:
                        raise Exception("Expected data, got nothing.")
                    httpreq.parse_http_stream(data)
                conn.sendall(httpreq.process(self.folder, self.handlers))



