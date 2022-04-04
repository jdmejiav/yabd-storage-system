import socket
import json
import backup as bk
import os

# import thread module
from _thread import *
import threading

#print_lock = threading.Lock()

resources=[]

def extract_ip():
    st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:       
        st.connect(('10.255.255.255', 1))
        IP = st.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        st.close()
    return IP

def receive_message(self,client_socket):
    data = ''.encode()
    try:
        message_header = client_socket.recv(self["HEADER_LENGTH"])
        
        message_length = int(message_header.decode("utf-8").strip())
        while len(data)<message_length:
            data += client_socket.recv(30000)    
    except:
        pass
    return data

def return_data(data:dict,self,con):
    message_header=b''
    res_name=data["key"]
    f = open(f'{os.getcwd()}/resources/{res_name}', "r")
    file = f.read()
    message=file.encode("utf-8")
    message_header = f"{len(message):<{30}}".encode("utf-8")
    con.send(message_header+message)
    print(con.recv(30000).decode())

def threaded(self,con):
    key = receive_message(self,con)
    decoded = key # b'data to be encoded'
    dict = json.loads(decoded)
    method=dict['method']
    if(method=='POST'):
        decoded2=dict["body"]
        with open(f'{os.getcwd()}/resources/{dict["name"]}', "w") as new_file:
            new_file.write(decoded2)
        resources.append(dict["name"])
        bk.save(resources,'resources')
        con.sendall(b'Funciona Pa')
    elif(method=='GET'):
        print("require resources")
        return_data(dict,self,con)        

def delete(dict,self,con):
    print("Deleting")
    print(dict)
    key=dict['key']
    if key in resources:
        dir = f'{os.getcwd()}/resources/{key}'
        if bk.delete_f(dir):
            resources.remove(key)
            bk.save(resources,'resources')
            res = {
                "message":"Sucess!! key deleted",
                "status": 1
            }  
            res_json = json.dumps(res) 
            res_json = res_json.encode("utf-8")  
            message_header = f"{len(res_json):<{30}}".encode("utf-8")
            con.send(message_header+res_json)
            print(con.recv(1024))
    else:
        res = {
            "message":"Failed!! key not found",
            "status":-2
        }  
        res_json = json.dumps(res) 
        res_json = res_json.encode("utf-8")  
        message_header = f"{len(res_json):<{30}}".encode("utf-8")
        con.send(message_header+res_json)
        

def listener_sock(self):
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    server_socket.bind((self["HOST"],self["PORT"]))
    server_socket.listen(5)
    print("Listening")
    while True:
        con,addr = server_socket.accept()

        # lock acquired by client
        print('Connected to :', addr[0], ':', addr[1])

        key = receive_message(self,con)
        decoded = key # b'data to be encoded'
        dict = json.loads(decoded)
        method=dict['method']
        if(method=='POST'):
            decoded2=dict["body"]
            with open(f'{os.getcwd()}/resources/{dict["name"]}', "w") as new_file:
                new_file.write(decoded2)
            resources.append(dict["name"])
            bk.save(resources,'resources')
            con.sendall(b'Funciona Pa')
        elif(method=='GET'):
            print("require resources")
            return_data(dict,self,con) 
        elif(method=='DELETE'):
            delete(dict,self,con)
        #print_lock.release() 


def reveal_to_leader(self): 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((self["LEADER_IP"],self["LEADER_PORT"]))
    client_socket.setblocking(False)
    
    message = ''

    getMessage ={   
        "ip":self["HOST"],
        "nodeName":self["HOSTNAME"],
        "port":self["PORT"],
        "method":"reveal"
    }
    message = json.dumps(getMessage)

    if message:
        message = message.encode("utf-8")
        length=self["HEADER_LENGTH"]
        message_header = f"{len(message):<{length}}".encode("utf-8")
        print(message)
        client_socket.send(message_header+message)

def udp_serv(self):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the port
    server_address = (self["HOST"],self["PORT"])
    print('starting up on {} port {}'.format(*server_address))
    sock.bind(server_address)
    while True:
        #print('\nwaiting to receive message')
        data, address = sock.recvfrom(4096)

        #print('received {} bytes from {}'.format(len(data), address))
        #print(data)

        if data:
            sent = sock.sendto(b'pong', address)
            #print('sent {} bytes back to {}'.format(sent, address))
        #print_lock.release() 

def create_folder():
    if not os.path.exists(f"{os.getcwd()}/resources"):
        os.makedirs(f"{os.getcwd()}/resources")

if __name__ == '__main__':
    data_f_names='resources'
    if(bk.file_exists(data_f_names)):
        resources = bk.get(data_f_names)

    create_folder()

    self={
        "LEADER_IP":'192.168.0.141',
        "LEADER_PORT":8001,
        "HOSTNAME" : socket.gethostname(),
        "HOST" : extract_ip(),
        "PORT":8888,
        "HEADER_LENGTH": 30,
    }
    reveal_to_leader(self)
    #print_lock.acquire()
    #listener_sock(self)
    th1= threading.Thread(target=listener_sock,
        args=(self,),
    ).start()
    th2=threading.Thread(target=udp_serv,
        args=(self,),
    ).start()
    
    #start_new_thread(udp_serv, (self,))
    #listener_sock(self)