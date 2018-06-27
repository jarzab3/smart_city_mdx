class Encoder:
    def __init__(self, name, svcId, debug=False):
        self.name = name
        self.svcId = svcId
        self.debug = debug

    def request(self, time_interval):
        sendRequest(self.svcId, time_interval)

    def process_response(self, message):
        # A response for a message is something like "@E,e,2,{3000:110,3100:120}"
        if message[3] != self.__TAG_ENCODER_RESPONSE:
            # FIXME: improve error checking
            # We have received a message but it is not an encoder reporting event
            sys.stdout.write("Distance message received but I don't know how to process it: {}\n".format(message))
        else:
            if self.debug:
                print ("DEBUG: received message is {}\n".format(message))
            # enc_values = message[message.indexOf("{")+1: message.indexOf("}")].split(",")
            enc_values = message[message.index("{")+1: message.index("}")].split(",")
            self._pulse = int(enc_values[self._encoderID].split(':')[0])
            c = int(enc_values[self._encoderID].split(':')[1])
            self._count += c
            if self.debug:
                print("DEBUG: count and pulse to: {} {} {}\n".format(c,self._pulse,self._count))