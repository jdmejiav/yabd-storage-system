# import socket programming library
from re import T
import socket
import json
# import thread module
from _thread import *
import threading
from time import sleep
import backup as bk

print_lock = threading.Lock()
resources = {}
nodes = {'l':{},'f':{}}
def get(c,msg:dict):
    if msg['key'] not in resources:
        raise ValueError('Warning!! key not found')
    else:
        data_key = msg['key']
        resources_file=json.dumps({"data":[resources,nodes]})
        print(resources_file)
        resources_file = resources_file.encode("utf-8")  
        message_header = f"{len(resources_file):<{30}}".encode("utf-8") 
        c.send(message_header+resources_file)


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

def receive_message(HEADER_LENGTH,client_socket):
    data = ''.encode()
    try:
        message_header = client_socket.recv(HEADER_LENGTH)        
        message_length = int(message_header.decode("utf-8").strip())
        while len(data)<message_length:
            data += client_socket.recv(30000)    
    except:
        pass
    return data

def leader_tables(HOST,PORT):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST,PORT))
    server_socket.listen(5)
    print("Listening")
    while True:
        con,addr = server_socket.accept()

        # lock acquired by client
        #print('Connected to :', addr[0], ':', addr[1])
        try:
            decoded = receive_message(30,con)
            res = json.loads(decoded)
            res2 = res['data']
            global resources
            resources = res2[0]
            global nodes
            nodes = res2[1]
            print(nodes)
            bk.save(resources,'resources')
            bk.save(nodes,'peers')
        except:
            print('fail')

# thread function
def threaded(c):
    try:
        data = ''.encode()
        message_header=b''
        HEADER_LENGTH = 30
        try:
            message_header = c.recv(HEADER_LENGTH)
            
            message_length = int(message_header.decode("utf-8").strip())
            while len(data)<message_length:
                data += c.recv(30000) 
            print_lock.release() 
        except:
            print_lock.release() 
            pass

        dict = json.loads(data)

        if(dict["method"] == "GET"):
            try:
                print("Require resources from the user")
                get(c,dict)
            except ValueError as e:
                error={"status":-1,"message":str(e)}
                message_header = f"{len(error):<{30}}".encode("utf-8")
                c.send(message_header+json.dumps(error).encode())  
        else:
            c.send(b'0')  
        # connection closed
        c.close()
        #print(len(message_header))       
    except:
        pass

def Main(HOST,PORT):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    print("socket binded to port", PORT)
 
    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")
 
    # a forever loop until client wants to exit
    while True:
 
        # establish connection with client
        c, addr = s.accept()
 
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
 
        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()

if __name__ == '__main__':
    host = extract_ip()
    port_for_leader = 8002
    port_for_client = 8000
    nodes_f_names='peers'
    if(bk.file_exists(nodes_f_names)):
        nodes = bk.get(nodes_f_names)
    resources_f_names='resources'
    if(bk.file_exists(resources_f_names)):
        resources = bk.get(resources_f_names)
    #Main()
    th1= threading.Thread(target=Main,
        args=(host,port_for_client),
    ).start()
    th2=threading.Thread(target=leader_tables,
        args=(host,port_for_leader),
    ).start()
