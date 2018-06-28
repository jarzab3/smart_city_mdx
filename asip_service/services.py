import asip
from settings import logging as log
import sys


class Encoders:
    def __init__(self, name: str, svc_id: str, debug: bool=False):
        self.name = name
        self.svc_id = svc_id
        self.debug = debug
        self.left_values = None
        self.right_values = None
        self.TAG_ENCODER_RESPONSE = asip.id_ENCODER_SERVICE

    def process_response(self, message: str) -> None:
        """
        This function is taking an input, validating by comparing an service tag and id and extracts values
        A response for a message is something like "@E,e,2,{3000:110,3100:120}"
        :param message:
        :return:
        """
        if message[1] != self.TAG_ENCODER_RESPONSE:
            # TODO error checking
            # TODO check if svcID is correct in response message
            # We have received a message but it is not an encoder reporting event
            log.error("Unable to process received message: {}".format(message))
        else:
            try:
                enc_values = message[message.index("{")+1: message.index("}")].split(",")
                self.left_values = [int(i) for i in enc_values[0].split(":")]
                self.right_values = [int(i) for i in enc_values[1].split(":")]
                if self.debug:
                    print("Encoders values. Left: {} Right: {}".format(self.left_values, self.right_values))
            except ValueError:
                log.error("Error while reading encoder value: %s" % message)

class Motor:
    def __init__(self, name: str, svc_id: str, motor_id: int, conn, debug: bool=False):
        self.name = name
        self.svc_id = svc_id
        self.debug = debug
        self.motor_id = motor_id
        self.header = asip.id_MOTOR_SERVICE  # M
        self.conn = conn

    # TODO Check if serial is open
    def send_request(self, motor_power: int) -> None:
        """
        Function is sending a serial request to Arduino, in order to set motor speed
        :param motor_power:
        :return None:
        """
        request_string = str(self.header + ',' + self.svc_id + ',' + str(self.motor_id) + ',' +
                             str(motor_power) + '\n').encode()
        if self.conn.is_open():
            if self.debug:
                log.debug("Request for motor: {} send request message: {}".format(self.motor_id,
                                                                                  request_string.decode().strip("\n")))
            successfully_sent_message = self.conn.send(request_string)
            if not successfully_sent_message:
                log.error("Error while requesting motor speed")
        else:
            log.error("Serial connection is closed. Please check serial device")
            sys.exit()

    def set_motor(self, speed: int) -> None:
        """
        Function in which speed value is being validate in terms of range and type, then send request is being made
        :param speed:
        :return:
        """
        # Example "M,m,0,50"
        # Speed should be between -100 and +100
        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100
        if self.debug:
            log.debug("Setting motor id:{} to speed:{}".format(self.motor_id, speed))
        self.send_request(speed)


    # Stop the motor (just set speed to 0)
    def stop_motor(self) -> None:
        """
        Stop motor by sending 0 value to a motor
        :return:
        """
        self.set_motor(0)
