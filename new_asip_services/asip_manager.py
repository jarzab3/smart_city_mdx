#!/usr/bin/python
from serialConnector import SerialConnection
import asip
import threading
from Services import *
from time import sleep
import time


class AsipManager:
    def __init__(self):
        self.isReady = False
        self.conn = SerialConnection()
        self.ports = self.conn.list_available_ports()
        self.selected_port = self.ports[0]
        self.debug = True
        self.run_event = None
        self.all_services = {}
        self.all_threads = []
        if self.debug:
            print("Available ports: {}".format(self.ports))
        if not self.isReady:
            self.open_serial()
        print("Serial port: %s opened successfully" % self.selected_port)

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

    def close_serial(self):
        self.conn.close()
        self.isReady = False

    def send_request(self, svcID, value):
        if self.isReady:
            request_string = str(svcID + ',' + asip.tag_AUTOEVENT_REQUEST + ',' + str(value) + '\n').encode()
            if self.debug:
                print("Request for svc %s msg: %s" % (svcID, request_string))
            successfully_sent_message = self.conn.send(request_string)
            if not successfully_sent_message:
                self.closePort()  # send failed so close port
        else:
            print('Serial port is not connected')

    def msg_dispatcher(self, msg):
        # print (msg)
        if len(msg) > 0:
            msg_head = msg[0]
        else:
            print(msg)
            msg_head = ""
            sleep(1)

        # print (msg[1])
        if msg_head == asip.EVENT_HEADER:
            if msg[1] == asip.SYSTEM_MSG_HEADER:
                print(msg[5:-1])
            else:
                # self.event_dispatcher(msg[1], msg[8:-2])
                self.event_dispatcher(msg)
        elif msg_head == asip.DEBUG_MSG_HEADER:
            # print ("Debug msg")
            # print(msg[1:])
            # Todo add debug message
            pass
        elif msg_head == asip.ERROR_MSG_HEADER:
            print ('Err: ' + msg[1:])

    def event_dispatcher(self, msg):
        id = msg[1]
        if id == asip.id_ENCODER_SERVICE:
            encoders = self.all_services.get('encoders')
            encoders.process_response(msg)

        elif id == asip.id_BUMP_SERVICE:
            print('Bump')
        elif id == asip.id_IR_REFLECTANCE_SERVICE:
            print('Reflectance')

    def run_services(self, run_event):
        while run_event.is_set():
            received_message = self.conn.get_buffer()
            self.msg_dispatcher(received_message)
            sleep(0.001)

    def initialize_services(self):
        """
        :return:
        """
        # Add encoders service
        encoders = Encoders(name="Encoders", svcID=asip.id_ENCODER_SERVICE, debug=False)
        # Enable all encoders by writing value 1, if you wish to disable you can do it by writing 0
        self.send_request(encoders.svcID, 1)
        self.all_services.update({'encoders': encoders})

        # Add motors service
        motor_1 = Motor(name="Left Motor", svcID=asip.tag_SET_MOTOR, id=0, conn=self.conn, debug=True)
        motor_2 = Motor(name="Left Motor", svcID=asip.tag_SET_MOTOR, id=1, conn=self.conn, debug=True)
        self.all_services.update({'motor_1': motor_1})
        self.all_services.update({'motor_2': motor_2})

    def initialize_main(self):
        self.run_event = threading.Event()
        self.run_event.set()
        main_thread = threading.Thread(name='Teensy msgs receiver', target=self.conn.receive_data, args=(self.run_event,))
        run_services_thread = threading.Thread(name='Services process', target=self.run_services,
                                               args=(self.run_event,))
        # Init all services
        self.initialize_services()
        self.all_threads = [main_thread, run_services_thread]
        # Start all threads
        for thread in self.all_threads:
            thread.start()
            time.sleep(.5)
            print("Thread: %s set up successfully" % thread.getName())

    def terminate_all(self):
        self.run_event.clear()
        for thread in self.all_threads:
            thread.join()
            print("Thread run status: {}: {}".format(thread.getName(), str(thread.is_alive())))

        self.close_serial()

# motors = Motor(root,'Motor Control', ('Left', 'Right'))
# encoders = Encoder(root,'Encoders',asip.id_ENCODER_SERVICE, ('Left', 'Right'))
# bump = Service(root,'Bump Sensors',asip.id_BUMP_SERVICE, ('Left', 'Right'))
# reflectance = Service(root,'Reflectance Sensors',asip.id_IR_REFLECTANCE_SERVICE,('Left', 'Center','Right'))

# def showInfo(msg):
#     info = msg.split(',')
#     msg = 'ASIP version %s.%s running on %s using sketch: %s' % (info[0], info[1], info[2], info[4])
#     logMsg(msg)
