# Yabd-storage-system FOLLOWER

# Setup

To run the Follower follow these steps, remember to install python version 3 suggested 3.8 or above

## Follower setup

The only step that you need to follow is to install python version 3, Follower only uses Python 3 vanilla build-in libraries 

# Usage

Once you run the command you need to execute this command on your CLI.

```bash
Windows: python follower.py
Linux: python3 follower.py
```

## Exit

Windows: close the terminal o kill the process (sockets are blocking) you cannot use control + c

Linux: close the terminal, kill the process or press control + c

# Remember

Follower runs once per operating system or machine due to the IP that is the key for the leader, also if the leader use another ip you need to update this information on the self code

```python
self={
        "LEADER_IP":'192.168.0.141', #Update ip here
        "LEADER_PORT":8001,
        "HOSTNAME" : socket.gethostname(),
        "HOST" : extract_ip(),
        "PORT":8888,
        "HEADER_LENGTH": 30,
    }
```
