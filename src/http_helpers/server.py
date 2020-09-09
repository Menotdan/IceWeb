import socket
import src.http_helpers.request_parser
import src.http_helpers.file_loader
import os

class Server:
    def __init__(self, address, https, webdirectory):
        self.socket = None
        self.webdirectory = webdirectory
        self.address = address
        self.port = 80

        if https:
            print("HTTPS not supported! Exiting.")
            exit(1)
        else:
           self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Open a TCP socket
        print("HTTP server created with webdirectory " + self.webdirectory)

    def bind_socket(self):
        try:
            self.socket.bind((self.address, self.port))
        except BaseException as e:
            print("Socket binding failed, exiting.")
            print(e)
            exit(1)

    def get_request(self, client):
        try:
            data = ""
            while True:
                packet = client.recv(1024)
                data += packet.decode("UTF-8")
                if "\r\n\r\n" in data:
                    break
            return data
        except BaseException as e:
            print("Server crashed!")
            print(e)
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except BaseException as E:
                print("Socket close failed.")
                print(E)
            exit(1)
    
    def send_response(self, client, response):
        client.sendall(response)

    def run_server(self):
        self.socket.listen(50)

        try:
            while True:
                print("Waiting for a new connection...")
                client,addr = self.socket.accept()
                print("Connection from " + str(addr) + ".")
                request = self.get_request(client)

                request = src.http_helpers.request_parser.Request(request)
                request.parse()
                print(request.request)
                stuff = request.request.split(" ")

                response_string = ""
                data = "hello".encode("UTF-8")
                content_type = "text/plain"
                if stuff[0] == "GET":
                    print("GET request for " + stuff[1])
                    file = stuff[1]
                    if "." not in file:
                        file = os.path.join(file, "index.html")
                    print(self.webdirectory)
                    file = os.path.join(self.webdirectory, file[1:])
                    print("Attempting to load file " + file)

                    if os.path.isfile(file):
                        loader = src.http_helpers.file_loader.FileLoader(file)
                        loader.load()
                        data = loader.contents
                        content_type = loader.mime_type
                        request.status = "HTTP/1.1 200 OK"
                    else:
                        request.status = "HTTP/1.1 404 Not Found"
                        content_type = "text/html"
                        data = ("<html>\n  <body>\n    404 not found\n    <br>" + stuff[1] + " not found.\n  </body>\n</html>").encode("UTF-8")
                else:
                    print("Unsuported method " + stuff[0])
                    request.elements = []
                    request.status = "HTTP/1.1 505 Unsupported Method" # lol
                
                request.elements = []
                request.elements.append(["Server", "IceWeb"])
                request.elements.append(["Content-Length", str(len(data))])
                request.elements.append(["Content-Type", content_type])
                request.create()
                response_string = request.string
                self.send_response(client, response_string.encode("UTF-8") + data)

                client.shutdown(socket.SHUT_RDWR)
                client.close()
        except BaseException as e:
            print("Server crashed!")
            print(e)
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
                self.socket.close()
            except BaseException as E:
                print("Socket close failed.")
                print(E)
            exit(1)
