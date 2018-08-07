# server.py 
import socket
import time

# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)


# get local machine name
host = socket.gethostname()
host = "0.0.0.0"

port = 9999

# bind to the port
serversocket.bind((host, port))
print("Server waiting for connection to {} port: {}".format(host, port))

# Queue up to 5 requests
serversocket.listen(5)
# Here is waiting for a connection
# print(serversocket)
clientsocket, addr = serversocket.accept()
clientsocket.setblocking(0)

i = 0
try:
    while i < 10:
        # Establish a connection
        print("Send msg to %s" % str(addr))
        currentTime = time.ctime(time.time()) + "\r\n"
        clientsocket.send(currentTime.encode('ascii'))
        i = + 1
        time.sleep(1)

    else:
        clientsocket.close()

except KeyboardInterrupt:
    clientsocket.close()
    serversocket.close()
    print("Closing connection")


