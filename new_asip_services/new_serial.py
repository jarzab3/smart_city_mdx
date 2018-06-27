#!/usr/bin/python
from serialConnector import SerialConnection
import asip
import threading


class AsipManager:
    def __init__(self):
        self.isReady = False
        self.conn = SerialConnection()
        self.ports = self.conn.list_available_ports()
        self.selected_port = self.ports[0]
        self.debug = True
        if self.debug:
            print("Available ports: {}".format(self.ports))
        if not self.isReady:
            self.open_serial()

    def on_open(self):
        if self.conn.is_open():
            self.close_serial()
        else:
            self.open_serial()

    def open_serial(self):
        baud_rate = 57600
        my_port = self.selected_port
        self.conn.open(my_port, baud_rate)
        if self.conn.is_open():
            if self.conn.send(asip.INFO_REQUEST.encode()):
                self.isReady = True
        else:
            print("Failed to open serial port")
            # logMsg('Failed to open serial port')

    def close_serial(self):
        self.conn.close()
        self.isReady = False


class Motor:

    def __init__(self):
        pass

    def onChangeM0(self, value):
        self.onChangeMotor('0', value)

    def onChangeM1(self, value):
        self.onChangeMotor('1', value)

    def onChangeMotor(self, motor, value):
        global isReady
        if isReady:
            print('Motor ' + motor + ' value= ' + value)
            if serialConnector.send('M,m,' + motor + ',' + value + '\n') == False:
                commsUI.closePort()  # send failed so close port
        else:
            print('Not ready')


def stopMotors(self):
    self.m0.set(0)
    self.m1.set(0)


class Encoder:
    def __init__(self, name, svcId):
        self.name = name
        self.svcId = svcId

    def request(self, time_interval):
        sendRequest(self.svcId, time_interval)


class Service:
    def request(self):
        t = self.entReq.get()
        sendRequest(self.svcId, t)


class Log:
    def insert(self, msg):
        self.log.insert(0, msg)


def sendRequest(svcId, value):
    if isReady:
        print('Request for svc ' + svcId + ': ' + str(value))

        request_string = str(svcId + ',' + asip.tag_AUTOEVENT_REQUEST + ',' + str(value) + '\n').encode()

        print (request_string)

        successfully_sent_message = serialConnector.send(request_string)

        if not successfully_sent_message:
            commsUI.closePort()  # send failed so close port
    else:
        print('Serial port is not connected')

def logMsg(msg):
    print(msg)
    log.insert(msg)


def msgDispatcher(msg):
    # logMsg(msg)
    if msg[0] == asip.EVENT_HEADER:
        if msg[1] == asip.SYSTEM_MSG_HEADER:
            showInfo(msg[5:-1])
        else:
            evtDispatcher(msg[1], msg[8:-2])
    elif msg[0] == asip.DEBUG_MSG_HEADER:
        logMsg(msg[1:])
    elif msg[0] == asip.ERROR_MSG_HEADER:
        logMsg('Err: ' + msg[1:])


def showInfo(msg):
    info = msg.split(',')
    msg = 'ASIP version %s.%s running on %s using sketch: %s' % (info[0], info[1], info[2], info[4])
    logMsg(msg)


def evtDispatcher(id, values):
    # print values
    fields = values.split(',')
    for index, f in enumerate(fields):
        if id == asip.id_ENCODER_SERVICE:
            subField = f.split(':')
            encoders.fieldVars[index][0].set(subField[0])
            encoders.fieldVars[index][1].set(subField[1])
            print('Encoder')
        elif id == asip.id_BUMP_SERVICE:
            bump.fieldVars[index].set(f)
            print('Bump')
        elif id == asip.id_IR_REFLECTANCE_SERVICE:
            reflectance.fieldVars[index].set(f)
            print('Reflectance')

def main():
    am = AsipManager()
    main_thread = threading.Thread(name='Teensy talker', target=am.conn.receive_data)
    get_buffer = threading.Thread(name='Get buffer', target=am.conn.get_buffer)
    main_thread.start()
    get_buffer.start()

# root.title("ASIP Mirto Tester")
# serialConnector.init(msgDispatcher)
# root.after(100, serialConnector.poll) # serial polling routine
# root.mainloop()
# t = threading.Thread(target=worker, args=(i,))
# main_thread = threading.Thread(name='Teensy talker', target=serialConnector.poll)
# main_thread.start()
# serialConnector.poll()


# global root
# root = Tk()
global isReady
isReady = False
# commsUI = SerialUI(root, 'Serial Port')

# motors = Motor(root,'Motor Control', ('Left', 'Right'))
# encoders = Encoder(root,'Encoders',asip.id_ENCODER_SERVICE, ('Left', 'Right'))
# bump = Service(root,'Bump Sensors',asip.id_BUMP_SERVICE, ('Left', 'Right'))
# reflectance = Service(root,'Reflectance Sensors',asip.id_IR_REFLECTANCE_SERVICE,('Left', 'Center','Right'))

# Distance = Service(root,'Distance Sensor',('distance',))

# log = Log(root)

# if __name__ == '__main__':
    # main()