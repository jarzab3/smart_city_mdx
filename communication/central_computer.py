# client.py
import socket
from time import sleep

# Create a socket object

# Get an IP address for given hostname
host = socket.gethostbyname("robot1")
print("Central unit waiting for connection to: {}".format(host))
port = 9999
chunk = 1024

i = 0
connected = False

while True:
    while not connected:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setblocking(0)
            s.connect((host, port))
            connected = True

        except socket.error:
            sleep(2)

    else:
        try:
            # Receive no more than 1024 bytes
            data = s.recv(chunk)
            if data:
                print("The time got from the server is %s" % data.decode('ascii'))
            else:
                connected = False
                print("Connection issue")
                sleep(2)

        except socket.error:
            connected = False
            print("Connection issue 1")
