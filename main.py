import sys
from follower import Follower
from leader import Leader
import asyncio
import threading


def main():
    PORT = 63333
    HOST = "127.0.0.1" 

    follower = Follower(HOST,PORT)
    follower2 = Follower(HOST,63334)
    leader = Leader(HOST,PORT)
    leader2 = Leader(HOST,63334)
    file = open("ejemplo.txt")
    f = str.encode(file.read())


    th = threading.Thread(target = leader.get_value, args=(f,))
    th = threading.Thread(target = leader2.get_value, args=(f,))
    th = threading.Thread(target = follower.handle_connection)
    th = threading.Thread(target = follower2.handle_connection)

    th.start()
    print ("Pues si funciona ejej")


    th.join ()
    
    
    

if __name__=='__main__':
    main()
