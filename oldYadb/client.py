import socket
import asyncio
import select

class client:
    async def handle_connection(self,msg):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sock.setbloquing(False)
        sock.connect_ex((self.HOST,self.PORT))
        sock.sendall(str.enconde(msg))
        data = ""
        try:
            while True:
                data +== await sock.recv(1024)
        except:
            pass
        return data
    
    def __init__(self, HOST, PORT):
        self.HOST = HOST
        self.PORT = PORT


if __name__=='__main__':
    
    asyncio.run()
