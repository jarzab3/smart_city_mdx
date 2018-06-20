from asip.services.asip_service import AsipService
import sys

class LCDService(AsipService):
    DEBUG = False
    _serviceID = 'L'

    __TAG_LCD_WRITE = 'W'
    __TAG_LCD_CLEAR = 'C'

    # A bump sensor has a unique ID (there may be more than one bump sensor attached, each one has a different bumpID)
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

    def set_LCD_message(self, message, line):
        if line > 4 or line < 0:
            sys.stdout.write("ERROR: line number ({}) not in range! (0-4)".format(line))
            return
        if self.DEBUG:
            sys.stdout.write("DEBUG: Writing: {} to line {} on the LCD\n".format(message,line))

        # Motors have been mounted the other way around, so swapping IDs 0 with 1 for id
        # self.asip.get_asip_writer().write(self._serviceID + ","
        #                                     + self.__TAG_SET_MOTOR_SPEED + ","
        #                                     + str(0 if self._motorID == 1 else 1)  # swapping
        #                                     + "," + speed)
        self.asip.get_asip_writer().write("{},{},{},{}\n".format(
            self._serviceID, self.__TAG_LCD_WRITE, str(line), message))

    def clear_LCD(self):
        if self.DEBUG:
            sys.stdout.write("DEBUG: Clearing the LCD")

        # Motors have been mounted the other way around, so swapping IDs 0 with 1 for id
        # self.asip.get_asip_writer().write(self._serviceID + ","
        #                                     + self.__TAG_SET_MOTOR_SPEED + ","
        #                                     + str(0 if self._motorID == 1 else 1)  # swapping
        #                                     + "," + speed)
        self.asip.get_asip_writer().write("{},{}\n".format(
            self._serviceID, self.__TAG_LCD_CLEAR))