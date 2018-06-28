import serial
from time import sleep
import sys
import glob


class SerialConnection:
    def __init__(self):
        self.ser = serial.Serial()
        # make our own buffer
        self.serBuffer = b''
        self.ser.timeout = 0  # Ensure non-blocking
        self.ser.writeTimeout = 0  # Ensure non-blocking

    def open(self, port, baud, timeout):
        if self.ser.isOpen():
            self.ser.close()
        self.ser.port = port
        self.ser.baudrate = baud
        self.ser.timeout = timeout
        self.ser.open()
        # Toggle DTR to reset Arduino
        self.ser.setDTR(False)
        sleep(1)
        # Toss any data already received
        self.ser.flushInput()
        self.ser.setDTR(True)

    def close(self):
        self.ser.close()

    def is_open(self):
        return self.ser.isOpen()

    def send(self, msg):
        if self.ser.isOpen():
            try:
                self.ser.write(msg)
                return True
            except (OSError, serial.SerialException):
                pass
        return False

    def receive_data(self, run_event):
        if not self.ser.isOpen():
            print ("Connection dropped, please check self.serial.")

        else:
            while run_event.is_set():
                try:
                    self.serBuffer = self.ser.readline()
                    sleep(0.01)
                except (OSError, serial.SerialException) as error:
                    print("Serial connection problem. %s" % error)

    def get_buffer(self):
        return self.serBuffer.decode('utf-8')

    def list_available_ports(self):
        """Lists self.serial ports

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of available self.serial ports
        """
        if sys.platform.startswith('win'):
            ports = ['COM' + str(i + 1) for i in range(256)]

        elif sys.platform.startswith('linux'):
            # this is to exclude your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')

        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')

        else:
            raise EnvironmentError('Unsupported platform')

        result = []

        for port in ports:
            try:
                self.ser.port = port
                self.ser.open()
                self.ser.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
            except IOError:
                pass

        return result
