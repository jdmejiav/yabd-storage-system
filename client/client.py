from dataclasses import dataclass
import socket
import json
import base64
from time import sleep
import os

from tkinter import filedialog
from alive_progress import alive_bar

def logo():
    print(r"""\
  /$$     /$$              /$$ /$$                 ╓▄▄▄▄▄▄,
|  $$   /$$/             | $$| $$                ╫█      ▐▓
 \  $$ /$$//$$$$$$   /$$$$$$$| $$$$$$$           ╫█▄▄▄▄▄▄▐▓
  \  $$$$/|____  $$ /$$__  $$| $$__  $$          ╫█      ▐▓
   \  $$/  /$$$$$$$| $$  | $$| $$  \ $$          ╓╙▀▀▀▀▀▀▀╝
    | $$  /$$__  $$| $$  | $$| $$  | $$        ,╣╜        ╙▓┐
    | $$ |  $$$$$$$|  $$$$$$$| $$$$$$$/       █▌            █▌
    |__/  \_______/ \_______/|_______/    ▄▀▀▀▀▀▀▓╕       ▄▀▀▀▀▀▀▄▄
                                         ╞▓▄▄▄▄▄ █▌      ╞▓▄▄▄▄▄▄ ▓
                                         ╞▓▄▄▄▄▄▄▓▌ΦΦΦΦ@m╞▓▄▄▄▄▄▄▄▓
                                          █▄     ▓▌      ▐▓       ▓
                                           ▀▀▀▀▀▀          ▀▀▀▀▀▀▀ 
    """)

def browseFiles():
        filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("All files",
                                                        "*.*"),
                                                        ("Text files",
                                                        "*.txt*"),
                                                        ("jpg files",
                                                        "*.jpg*"),
                                                        ("png files",
                                                        "*.png*"),
                                                        ("pdf files",
                                                        "*.pdf*")
                                                        ))
        return filename 

class Client:   

    def delete(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST,self.PORT))
        #client_socket.setblocking(False)

        key_obj = input("Enter key of the object to delete: ")

        message = ''

        getMessage ={   
            "key": key_obj,
            "method": "DELETE",
        }
        message = json.dumps(getMessage)

        message = message.encode("utf-8")
        message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)

        datarev=b''
        message_header = client_socket.recv(30)
        message_length = int(message_header.decode("utf-8").strip())
        while len(datarev)<message_length:
            res_data=client_socket.recv(30000)
            datarev+=res_data
        res=json.loads(datarev)
        if "status" in res:
            if res["status"] ==-1:
                print('\033[93m' + res["message"] + '\033[0m')
            elif res["status"] ==-2:
                print('\033[91m' + res["message"] + '\033[0m')
            else:
                print('\033[92m' +res["message"]+'\033[0m')
        client_socket.close()
        del client_socket
        return datarev

    def read(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST,self.PORT))
        #client_socket.setblocking(False)

        key_obj = input("Enter key of the object: ")

        message = ''

        getMessage ={   
            "key": key_obj,
            "method": "GET",
            "op":self.GETOPERATION 
        }
        message = json.dumps(getMessage)

        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)

        datarev=b''
        message_header = client_socket.recv(30)
        message_length = int(message_header.decode("utf-8").strip())
        with alive_bar(message_length,title=f'Downloading') as bar:   # default setting
            while len(datarev)<message_length:
                res_data=client_socket.recv(30000)
                datarev+=res_data
                bar(len(res_data)) 
            res=json.loads(datarev)
        if "status" in res:
            if res["status"] ==-1:
                print('\033[91m' + res["message"] + '\033[0m')
            else:
                if(res["ext"]!='./yadbdatatxt'):
                    with open(f'{res["name"]}{res["ext"]}', "wb") as new_file:
                            new_file.write(base64.b64decode(res['data']))
                    client_socket.close()
                    print('\033[92m' + "Success!! data saved on file "+res["name"]+res["ext"]+ '\033[0m')
                else:
                    print('\033[92m' + "Success!! data recovered" +'\033[0m')
                    print("Data->",base64.b64decode(res['data']).decode())
                    client_socket.close()
        del client_socket
        return datarev
    
    def update(self,datakey='',datavalue=''):
        message = ''
        if datakey == '':
            key_obj = input("Enter key of the object: ")
            key = key_obj.encode("utf-8")
            key_header = f"{len(key):<{self.HEADER_LENGTH}}".encode("utf-8")
            #path = input("Enter file path on your machine: ")
            print("Enter file path on your machine: ")
            path= browseFiles()
            name = ''
            extention = ''
            if '/' not in path:
                if '.' not in path:
                    name = path
                else:
                    idx = path.index('.')
                    name = path[:idx]
                    extention = path[idx:]
            else:
                idxb = path.rindex("/")+1
                path2 = path[idxb:]

                if '.' not in path2:
                    name = path2
                else:
                    idx = path2.index('.')
                    name = path2[:idx]
                    extention = path2[idx:]

            f = open(path,'rb')
            encoded =base64.b64encode(f.read())
            self.objects[key_obj] = {   
                                        "key": key_obj,
                                        "name": name,
                                        "extention": extention,
                                        "method": "UPDATE",
                                        "body": encoded.decode('ascii'),
                                    }
            message = json.dumps(self.objects[key_obj])
        else:
            encoded =base64.b64encode(datavalue.encode())
            self.objects[datakey] = {   
                                        "key": datakey,
                                        "name": "nameout",
                                        "extention": "./yadbdatatxt",
                                        "method": "UPDATE",
                                        "body": encoded.decode('ascii'),
                                    }
            message = json.dumps(self.objects[datakey])

        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST,self.PORT))
        #client_socket.setblocking(False)

        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)
            res=b''
            while True:
                data=client_socket.recv(30000)
                if not data:
                    break
                else:
                    res+=data
            res = json.loads(res)
            if "status" in res:
                if res["status"]==-1: 
                    print('\033[93m' + res["message"] + '\033[0m')
                elif res["status"]==-2:
                    print('\033[91m' + res["message"] + '\033[0m')
                else:
                    print('\033[92m' + res["message"] + '\033[0m')
        client_socket.close()
        del client_socket
        print('bye')
    def create(self,datakey='',datavalue=''):
        
        message = ''
        if datakey == '':
            key_obj = input("Enter key of the object: ")
            key = key_obj.encode("utf-8")
            key_header = f"{len(key):<{self.HEADER_LENGTH}}".encode("utf-8")
            #path = input("Enter file path on your machine: ")
            print("Enter file path on your machine: ")
            path= browseFiles()
            name = ''
            extention = ''
            if '/' not in path:
                if '.' not in path:
                    name = path
                else:
                    idx = path.index('.')
                    name = path[:idx]
                    extention = path[idx:]
            else:
                idxb = path.rindex("/")+1
                path2 = path[idxb:]

                if '.' not in path2:
                    name = path2
                else:
                    idx = path2.index('.')
                    name = path2[:idx]
                    extention = path2[idx:]
                    
            print(name)
            print(extention)

            f = open(path,'rb')
            encoded =base64.b64encode(f.read())
            self.objects[key_obj] = {   
                                        "key": key_obj,
                                        "name": name,
                                        "extention": extention,
                                        "method": "POST",
                                        "body": encoded.decode('ascii'),
                                    }
            message = json.dumps(self.objects[key_obj])
        else:
            encoded =base64.b64encode(datavalue.encode())
            self.objects[datakey] = {   
                                        "key": datakey,
                                        "name": "nameout",
                                        "extention": "./yadbdatatxt",
                                        "method": "POST",
                                        "body": encoded.decode('ascii'),
                                    }
            message = json.dumps(self.objects[datakey])
        print('\033[92m' + "Sending data" + '\033[0m')
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((self.HOST,self.PORT))
        #client_socket.setblocking(False)

        if message:
            message = message.encode("utf-8")
            message_header = f"{len(message):<{self.HEADER_LENGTH}}".encode("utf-8")
            client_socket.send(message_header + message)
            res=b''
            while True:
                data=client_socket.recv(30000)
                if not data:
                    break
                else:
                    res+=data
            res = json.loads(res)
            if "status" in res:
                if res["status"]==-1: 
                    print('\033[93m' + res["message"] + '\033[0m')
                elif res["status"]==-2:
                    print('\033[91m' + res["message"] + '\033[0m')
                else:
                    print('\033[92m' + res["message"] + '\033[0m')
        client_socket.close()
        del client_socket
        print('bye')
    
    def interface(self):
        while True:
            print("What you want to do? ")
            operation= input("Menu\nC for upload a file\nR for download a file\nU for update a file already exist\nD for delete a file alredy exist\nE for exit\n").upper()
            if(operation== "C" ):
                client.create()
            elif(operation== "R" ):
                client.read()
            elif(operation== "U" ):
                client.update()
            elif(operation== "D"):
                client.delete()
            elif(operation== "E"):
                os.system('clear' if os.name == 'nt' else 'clear')
                print("Bye :)")
                break
            else:
                print("Please press a valid key")
                sleep(2)
                client.interface()

    def __init__(self,HOST,PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.HEADER_LENGTH = 30
        self.GETOPERATION = 0
        self.objects = {}

if __name__=='__main__':
    client = Client("54.226.31.101",8001)
    logo()
    client.interface()