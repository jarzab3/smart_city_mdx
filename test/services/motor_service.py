from python_asip_client.services.asip_service import AsipService
import sys

class MotorService(AsipService):
    DEBUG = False
    _serviceID = 'M'
    # A motor has a unique ID (there may be more than one motor attached, each one has a different motorID)
    _motorID = ""
    asip = None  # The service should be attached to a client
    # An encoder has a unique ID (there may be more than one encoder attached, each one has a different encoderID)
    _encoderID = ""
    _count = 0  # Count for the encoder
    _pulse = 0  # Pulse for the encoder
    __TAG_ENCODER_RESPONSE = 'e'
    # Service constant
    __TAG_SET_MOTOR_SPEED = 'm'
    __TAG_RESET_ENCODER_COUNTS = 'E'

    # The constructor takes the id of the motor.
    def __init__(self, id, asipclient):
        AsipService.__init__(self)
        self._motorID = id
        self._encoderID = id
        self.asip = asipclient

    # *** Standard getters and setters ***

    def get_service_id(self):
        return self._serviceID

    def set_service_id(self,id):
        self._serviceID = id

    # receives an instance of AsipClient as parameter
    def set_client(self, client):
        self.asip = client

    def get_client(self):
        return self.asip

    def get_motor_id(self):
        return self._motorID

    def set_motor_id(self, id):
        self._motorID = id

    def enable_encoder(self):
        self.asip.get_asip_writer().write(
            "{},{},{}".format(self._serviceID, AsipService.AUTOEVENT_REQUEST, str(1)))

    def disable_encoder(self):
        self.asip.get_asip_writer().write(
            "{},{},{}".format(self._serviceID, AsipService.AUTOEVENT_REQUEST, str(0)))

    def process_response(self, message):
        # A response for a message is something like "@E,e,2,{3000:110,3100:120}"
        if message[3] != self.__TAG_ENCODER_RESPONSE:
            # FIXME: improve error checking
            # We have received a message but it is not an encoder reporting event
            sys.stdout.write("Distance message received but I don't know how to process it: {}\n".format(message))
        else:
            if self.DEBUG:
                sys.stdout.write("DEBUG: received message is {}\n".format(message))
            enc_values = message[message.index("{") + 1: message.index("}")].split(",")
            enc_values = [int(i) for i in enc_values[self._encoderID].split(":")]
            self._pulse = int(enc_values[0])
            self._count = int(enc_values[1])
            if self.DEBUG:
                sys.stdout.write("DEBUG: count: {} pulse: {}\n".format(self._count, self._pulse))

    def set_motor(self, speed):
        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100
        if self.DEBUG:
            sys.stdout.write("DEBUG: setting motor {} to {}\n".format(self._motorID, speed))

        # Motors have been mounted the other way around, so swapping IDs 0 with 1 for id
        # self.asip.get_asip_writer().write(self._serviceID + ","
        #                                     + self.__TAG_SET_MOTOR_SPEED + ","
        #                                     + str(0 if self._motorID == 1 else 1)  # swapping
        #                                     + "," + speed)
        self.asip.get_asip_writer().write("{},{},{},{}".format(
            self._serviceID, self.__TAG_SET_MOTOR_SPEED, 0 if self._motorID == 1 else 1, speed))

    # Stop the motor (just set speed to 0)
    def stop_motor(self):
        self.set_motor(0)

    def get_count(self):
        return self._count

    def get_pulse(self):
        return self._pulse

    def reset_count(self):
        self.asip.get_asip_writer().write(
            "{},{}".format(self._serviceID, self.__TAG_RESET_ENCODER_COUNTS))
