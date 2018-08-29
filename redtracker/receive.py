import urllib2
import numpy as np
import cv2
from time import sleep
from laser_tracker import LaserTracker


class StreamHandler:
    def __init__(self):
        self.url = 'http://0192.168.200.100:8000/stream.mjpg'
        self.tracker = LaserTracker()

    def receive_stream(self):
        stream = None
        # Try to initialised a stream connection. Note is case of 404 error, please check if stream source is running
        try:
            stream = urllib2.urlopen(self.url)
            print("Successfully opened a stream")
        except urllib2.HTTPError as e:
            code = e.code
            print("URLLIB error while opening a stream: %s" % code)
        # Init bytes value to which data from streaming can be appended and then converted to a frame
        bytes = ''
        if stream is not None:
            while True:
                try:
                    bytes += stream.read(1024)
                    a = bytes.find('\xff\xd8')
                    b = bytes.find('\xff\xd9')
                    if a != -1 and b != -1:
                        frame_bytes = bytes[a:b + 2]
                        bytes = bytes[b + 2:]
                        np_array = np.fromstring(frame_bytes, np.uint8)
                        frame = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
                        self.tracker.run(frame)

                    # Display the resulting frame
                    # cv2.imshow('frame',frame)

                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                except Exception as error:
                    print("Error while stream receiving: {}".format(error))
