import socket


class Leader:

    def get_value(self, msg):

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.HOST, self.PORT))
            s.sendall(b"Hello, world")
            data = s.recv(1024)
        print(f"lo que se mandó fue: {data}")
        


    def __init__(self, HOST , PORT):
        self.HOST = HOST
        self.PORT = PORT

