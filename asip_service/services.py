import asip


class Encoders:
    def __init__(self, name, svcID, debug=False):
        self.name = name
        self.svcID = svcID
        self.debug = debug
        self.left_values = None
        self.right_values = None
        self.TAG_ENCODER_RESPONSE = asip.id_ENCODER_SERVICE

    def process_response(self, message):
        # print (message)
        # A response for a message is something like "@E,e,2,{3000:110,3100:120}"
        if message[1] != self.TAG_ENCODER_RESPONSE:
            # TODO error checking
            # TODO check if svcID is correct in response message
            # We have received a message but it is not an encoder reporting event
            print("Unable to process received message: {}".format(message))
        else:
            try:
                enc_values = message[message.index("{")+1: message.index("}")].split(",")
                self.left_values = [int(i) for i in enc_values[0].split(":")]
                self.right_values = [int(i) for i in enc_values[1].split(":")]
                if self.debug:
                    print ("Encoders values. Left: {} Right: {}".format(self.left_values, self.right_values))
            except ValueError:
                print ("Error while reading encoder value: %s" % message)
class Motor:
    def __init__(self, name, svcID, id, conn, debug=False):
        self.name = name
        self.svcID = svcID
        self.debug = debug
        self.id = id
        self.header = asip.id_MOTOR_SERVICE  # M
        self.conn = conn

    # Check if serial is open
    def send_request(self, motor_power):
        request_string = str(self.header + ',' + self.svcID + ',' + str(self.id) + ',' + str(motor_power) + '\n').encode()
        if self.debug:
            print("Request for motor: {} send request: {}".format(self.id, request_string))
        successfully_sent_message = self.conn.send(request_string)
        if not successfully_sent_message:
            print ("Error while requesting motor speed")

    def set_motor(self, speed):
        # Example "M,m,0,50"

        # Speed should be between -100 and +100
        if speed > 100:
            speed = 100
        if speed < -100:
            speed = -100

        if self.debug:
            print("DEBUG: setting motor {} to {}".format(self.id, speed))

        self.send_request(speed)

    # Stop the motor (just set speed to 0)
    def stop_motor(self):
        self.set_motor(0)
