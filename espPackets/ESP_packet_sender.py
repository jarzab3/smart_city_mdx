import socket
from time import sleep
UDP_IP ="192.168.200.150"
UDP_PORT = 8888
MESSAGE = "H"
while 1:

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    sleep(2)
    MESSAGE = "L"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
    sock.sendto(bytes(MESSAGE, "utf-8"), (UDP_IP, UDP_PORT))
    sleep(8)
    MESSAGE = "H"
