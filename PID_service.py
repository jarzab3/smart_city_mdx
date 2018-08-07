from python_asip_client.services.asip_service import AsipService
import sys

class PIDService(AsipService):
    DEBUG = False
    _serviceID = 'M'

    __TAG_ONE_MOTOR = 'r'
    __TAG_BOTH_MOTORS = 'R'


    asip = None # The service should be attached to a client

    # The constructor takes the id of the bump sensor.
    def __init__(self, id, asipclient):
        AsipService.__init__(self)
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


    def process_response(self, message):
        # Do nothing for motors
        pass

    def set_Motor_RPM(self, motor_ID, RPM, duration):
        self.asip.get_asip_writer().write("{},{},{},{},{}\n".format(
            self._serviceID, self.__TAG_ONE_MOTOR, str(motor_ID), str(RPM), str(duration)))

    def set_Motors_RPM(self, RPM0, RPM1, duration):
        self.asip.get_asip_writer().write("{},{},{},{},{}\n".format(
            self._serviceID, self.__TAG_BOTH_MOTORS, str(RPM0), str(RPM1), str(duration)))

