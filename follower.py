import socket
import asyncio

class Follower:


    
    def handle_connection(self):                        #This is a server listening
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.bind((self.HOST,self.PORT))
        sock.listen()
        
        conn, addr = sock.accept()
        data  = bytes('')
        try: 
            while True:
                data += conn.recv(1024)
        except:
            pass
        conn.sendall(data)

    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT