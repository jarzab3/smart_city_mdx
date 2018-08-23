
class StreamHandler:
    def __init__(self):
        self.url = '192.168.200.100/stream.mjpeg'

    def receive_stream():
        stream = None

        # Try to initialised a stream connection. Note is case of 404 error, please check if stream source is running
        try:
            stream = urllib2.urlopen(self.url)
            log.info("Successfully opened a stream")

        except urllib2.HTTPError as e:

            code = e.code
            log.error("URLLIB error while opening a stream: %s" % code)

        # Init bytes value to which data from streaming can be appended and then converted to a frame
        bytes = ''

        if stream != None:
            while True:
                try:
                    bytes += stream.read(1024)
                    a = bytes.find('\xff\xd8')
                    b = bytes.find('\xff\xd9')
                    if a != -1 and b != -1:
                        frameBytes = bytes[a:b + 2]
                        bytes = bytes[b + 2:]
                        nparr = np.fromstring(frameBytes, np.uint8)
                        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                        cv2.imshow('asd', frame)

                except Exception as error:
                    print("Error while stream receiving: {}".format(error))


sh = StreamHandler
sh.receive_stream()