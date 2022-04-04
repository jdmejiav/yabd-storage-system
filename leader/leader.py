# import socket programming library
from re import T
import socket
import json
# import thread module
from _thread import *
import threading
from time import sleep
import partitionFile as pf 
import backup as bk

print_lock = threading.Lock()

nodes = {'l':{},'f':{}}
resources = {}
not_available = []
def ping_udp(host,port):
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (host, port)
    message = b'ping'
    sock.settimeout(5)
    
    try:
        # Send data
        #print('sending {!r}'.format(message))
        sent = sock.sendto(message, server_address)

        # Receive response
        #print('waiting to receive')
        data, server = sock.recvfrom(1024)
        #print('received {!r}'.format(data))
        nodes['f'][host][1]=1
        if(host in not_available):
            not_available.remove(host)
        bk.save(nodes,'peers')
    except socket.error:
        nodes['f'][host][1]=0
        if(host not in not_available):
            not_available.append(host)
        bk.save(nodes,'peers')
        #raise ValueError("Failed")
    finally:
        #print('closing socket')
        sock.close()

def get_states():
    while True:
        if len(nodes)>0:
            for key, value in nodes['f'].items():
                ping_udp(key,value[0])
            sleep(2)


def sendToFollowers(file,message_header,HOST,PORT):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.send(message_header+file)
        print(sock.recv(30000).decode())
        sock.close()

def ckeckList(lst):
  
    ele = 1
    chk = True
      
    # Comparing each element with first item 
    for item in lst:
        if ele != item:
            chk = False
            break
              
    if (chk == True): return True
    else: return False     

def delete(c,msg:dict):

    deleted_res=[]
    is_deleted=[]
    data = b''
    if msg['key'] not in resources:
        raise ValueError('Warning!! key not found')
    else:
        try:    
            data_key = msg['key']
            resources_file=resources[data_key]['resources']
            ip=nodes['f']
            for key, value in resources_file.items():
                node_to_get=()
                print(key,value)
                for i in value:
                    print(f'Removing key {key} from node {i}')
                    node_to_get=(i,ip[i][0])
                    getMessage ={   
                        "key": key,
                        "method": "DELETE",
                    }
                    message = json.dumps(getMessage)
                    message = message.encode("utf-8")
                    message_header = f"{len(message):<{30}}".encode("utf-8")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect(node_to_get)
                        sock.send(message_header + message)

                        print(f'connected with {value[0]}, {ip[value[0]][0]}')

                        message_header=b''
                        message_header = sock.recv(30)
                        message_length = int(message_header.decode("utf-8").strip())
                        data_node=''.encode()
                        while len(data_node)<message_length:
                            data_node += sock.recv(1024)
                        data+=data_node
                        sock.send(b'ok')                       
                        sock.close()
                        del sock
                        print(data)
                        dict = json.loads(data)
                        if "status" in dict :
                            if dict["status"]==1:
                                deleted_res.append(1)
                                #resources[data_key]['resources'][key].remove(i)
                                #bk.save(resources,'resources')
                            else:
                                deleted_res.append(0) 
                        else: 
                            raise ValueError('Error!! failed to remove the key')         
                    data=b''   
            is_the_same=ckeckList(deleted_res)
            if is_the_same:
                del resources[data_key]
                bk.save(resources,'resources')
                res = {
                    "message":"Success!! key removed",
                    "status":1
                }  
                res_json = json.dumps(res) 
                res_json = res_json.encode("utf-8")  
                message_header = f"{len(res_json):<{30}}".encode("utf-8") 
                c.send(message_header+res_json)
            elif is_the_same:
                res = {
                    "message":dict["message"],
                    "status":dict['status'],
                }  
                res_json = json.dumps(res) 
                res_json = res_json.encode("utf-8")  
                message_header = f"{len(res_json):<{30}}".encode("utf-8") 
                c.send(message_header+res_json)   
        except:
            raise ValueError('Error!! failed to remove the key')             
def get(c,msg:dict):
    print(msg)
    op=msg["op"]
    if(op==1):
        dict={
            "res":"ok",
            "result":1
        }
        c.send(json.dumps(dict).encode())
    elif(op==0):

        if msg['key'] not in resources:
            raise ValueError('Error!! key not found')
        else:
            try:    
                data_key = msg['key']
                resources_file=resources[data_key]['resources']
                data = ''.encode()
                for key, value in reversed(resources_file.items()):
                    ip=nodes['f']
                    node_to_get=()
                    i=0
                    while i <len(value):
                        if ip[value[i]][1]==1:
                            node_to_get=(value[i],ip[value[i]][0])
                            i=len(value)+1
                        i+=1

                    print(f'Recovering data from {node_to_get}')
                    getMessage ={   
                        "key": key,
                        "method": "GET",
                    }
                    message = json.dumps(getMessage)
                    message = message.encode("utf-8")
                    message_header = f"{len(message):<{30}}".encode("utf-8")
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.connect(node_to_get)
                        sock.send(message_header + message)

                        print(f'connected with {value[0]}, {ip[value[0]][0]}')

                        message_header=b''

                        message_header = sock.recv(30)
                        message_length = int(message_header.decode("utf-8").strip())
                        data_node=''.encode()
                        while len(data_node)<message_length:
                            data_node += sock.recv(30000)
                        sock.send(b'ok')                       
                        sock.close()
                        data+=data_node
                        del sock
            except:
                raise ValueError('Error!! failed to recover data')             

        res = {
            "name":resources[data_key]['name'],
            "ext":resources[data_key]['format'],
            "data":data.decode('ascii'),
            "status":1
        }  
        res_json = json.dumps(res) 
        res_json = res_json.encode("utf-8")  
        message_header = f"{len(res_json):<{30}}".encode("utf-8") 
        c.send(message_header+res_json)

def post(dict,servers,inf):
    names = list(dict.keys())  
    resources[inf["key"]]={"resources":{},"name":inf["name"],"format":inf["ext"]}
    print(f'recived {inf["name"]}{inf["ext"]}')
    file_resources={}
    for key, value in servers['f'].items():
        #key = ip
        #value = port,status
        if nodes['f'][key][1]==1:
            if(len(names)==0):
                names = list(dict.keys())
            name = names.pop()
            part={'name':name,'body':dict[name],'method':'POST'}
            if name not in file_resources:
                file_resources[name]=[]
            file_resources[name].append(key)
            filePart= json.dumps(part).encode()
            message_part_header= f"{len(filePart):<{30}}".encode("utf-8")
            sendToFollowers(filePart,message_part_header,key,value[0])             
    (resources[inf["key"]])["resources"]=file_resources
    bk.save(resources,'resources')

def update(c,msg:dict):
    data = b''
    if msg['key'] not in resources:
        raise ValueError('Warning!! key not found')
    else:
        inf={
            "key":msg["key"],
            "name":msg["name"],
            "ext":msg["extention"],
        }
        print("teas")
        dicPart=pf.splitFile(msg['body'],msg['name'],(len(nodes["f"])-len(not_available))//2,msg["key"])
        post(dicPart,nodes,inf) 

def get_node_inf(node_inf):
    if(node_inf["ip"] not in nodes["f"]):
        nodes["f"][node_inf["ip"]]=[node_inf["port"],1]
        bk.save(nodes,'peers')
    print(nodes)

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
        elif(dict["method"] == "reveal"):
            get_node_inf(dict)
        elif(dict["method"] == "POST"):  
            print("sending data") 
            try:
                inf={
                    "key":dict["key"],
                    "name":dict["name"],
                    "ext":dict["extention"],
                } 
                if inf["key"] in resources:
                    raise ValueError('Warning!! key already exists,-1')
    
                print("Partitioning data") 
                dicPart=pf.splitFile(dict['body'],dict['name'],(len(nodes["f"])-len(not_available))//2,dict["key"])
                try:
                    post(dicPart,nodes,inf)
                except:
                    raise ValueError('Error!! internal failure,-2')
                c.send(json.dumps({"status":1,"message":"Sucess!! data saved"}).encode())  
            except ValueError as e:
                vals= (str(e)).split(',')
                error={"status":int(vals[1]),"message":vals[0]}
                c.send(json.dumps(error).encode())  
        elif(dict["method"] == "DELETE"):
            try:
                delete(c,dict)
            except ValueError as e:
                error={"status":-1,"message":str(e)}
                message_header = f"{len(error):<{30}}".encode("utf-8")
                c.send(message_header+json.dumps(error).encode())  
        elif(dict["method"] == "UPDATE"):
            try:
                update(c,dict)
                c.send(json.dumps({"status":1,"message":"Sucess!! data updated"}).encode())  
            except ValueError as e:
                error={"status":-1,"message":str(e)}
                c.send(json.dumps(error).encode())  
        else:
            c.send(b'0')  
        # connection closed
        c.close()
        #print(len(message_header))       
    except:
        pass

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

def Main():
    host = extract_ip()
    print(host)
    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 8001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
 
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
    nodes_f_names='peers'
    if(bk.file_exists(nodes_f_names)):
        nodes = bk.get(nodes_f_names)
    resources_f_names='resources'
    if(bk.file_exists(resources_f_names)):
        resources = bk.get(resources_f_names)
    #Main()
    th1= threading.Thread(target= Main).start()
    th2= threading.Thread(target=get_states).start()