# server.py 
import socket
from python_asip_client.boards.serial_board import SerialBoard
from time import sleep
import sys


class TCPHandler:

    def __init__(self):
        # Create a socket object
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host = socket.gethostname()
        self.host = "0.0.0.0"
        self.port = 9999
        self.chunk = 1024
        # Bind to the port
        self.serversocket.bind((self.host, self.port))
        print("Server waiting for connection to {} port: {}".format(self.host, self.port))
        # Queue up to 5 requests
        self.serversocket.listen(5)
        # Here is waiting for a connection
        self.clientsocket, self.addr = self.serversocket.accept()
        self.clientsocket.setblocking(1)

    def receive(self):
        try:
            # Receive no more than 1024 bytes
            data = self.clientsocket.recv(self.chunk)
            if data:
                return data
        except socket.error as error:
            sys.stdout.write("Error while receiving data. Error: {}".format(error))

    def send_data(self, message):
        try:
            message_to_send = message.encode()
            self.clientsocket.sendall(message_to_send)

        except socket.error as error:
            self.clientsocket.close()
            self.serversocket.close()
            sys.stdout.write("Error while sending a data. Error: {}".format(error))
            sys.exit()

        except KeyboardInterrupt:
            self.clientsocket.close()
            self.serversocket.close()
            sys.stdout.write("Closing connection")

    def run_bridge(self, _serial_writer):
        while True:
            try:
                response = self.receive().decode()
                _serial_writer.write(response)
                sleep(0.0001)
            except socket.error as error:
                self.clientsocket.close()
                self.serversocket.close()
                sys.stdout.write("TCP error: {}".format(error))


def run_tcp_bridge():
    tcp_handler = TCPHandler()
    serial_board = SerialBoard(tcp_handler)
    serial_writer = serial_board.get_asip_client().get_asip_writer()
    tcp_handler.run_bridge(serial_writer)


if __name__ == '__main__':
    run_tcp_bridge()
