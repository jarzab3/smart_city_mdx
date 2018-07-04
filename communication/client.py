# client.py  
import socket
from time import sleep

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostbyname("robot1")
print("Client send request to host: {}".format(host))
port = 9999
# connection to hostname on the port.
s.connect((host, port))


i = 0

while True:
    # Receive no more than 1024 bytes
    tm = s.recv(1024)
    print("The time got from the server is %s" % tm.decode('ascii'))
else:
    s.close()
    print("Closing connection")
