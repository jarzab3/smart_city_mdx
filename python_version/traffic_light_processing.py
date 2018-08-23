__author__ = "Daniel"
__copyright__ = "Copyright 2018, Middlesex University"
__credits__ = ["Adam Jarzebak", ]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Daniel"
__email__ = ""
__status__ = "Development"

import requests
import base64
import json
import sys
from picamera import PiCamera
from time import sleep
from python_asip_client.serial_mirto_robot import SerialMirtoRobot
from python_asip_client.mirto_robot import MirtoRobot
import os
import glob


class TrainDetector:
    def __init__(self):
        # Init a camera using PiCamera module
        self.camera = PiCamera()
        self.train_images_directory = 'images/'
        # Init robot features
        services = SerialMirtoRobot()
        services = services.get_services()
        self.mirto = MirtoRobot(services)

    def take_pics_from_camera(self, number_of_picture_to_take=50):
        """
        Takes a certain n amount of pictures in order to provide pictures to train the AI
        :param number_of_picture_to_take: int
        :return:
        """
        interrupt = 0.2
        start_in = list(range(0, 7))
        start_in.sort(reverse=True)
        self.mirto.clear_lcd()
        for s in start_in:
            self.mirto.set_lcd_message("Start training in: %s sec" % s, 1)
            sleep(1)
        self.mirto.clear_lcd()
        for picture in range(0, number_of_picture_to_take):
            try:
                self.camera.capture(self.train_images_directory + 'capture_%s.jpg' % picture)
                sleep(interrupt)
                self.mirto.set_lcd_message("Picture taken: %s" % picture, 0)
                print("Picture taken: %s" % picture)
                sleep(interrupt)
            except KeyboardInterrupt:
                print('Keyboard interrupt exiting')
                sys.exit(0)
        print("Finish training")
        del self.mirto
        sys.exit(0)


class TrafficLightDetector:
    def __init__(self):
        self.camera = PiCamera()
        self.run_image_directory = 'live_images/image.jpg'
        services = SerialMirtoRobot()
        services = services.get_services()
        self.mirto = MirtoRobot(services)
        self.mirto.clear_lcd()

    def what_color_is(self):
        """
        Tells the colour of the traffic light
        :return: color detected
        """
        sleep(0.5)

        files = glob.glob('live_images/*')
        for f in files:
            os.remove(f)
        print("Cleaning directory")
        self.camera.capture(self.run_image_directory)
        print("Picture taken ..... ")
        url = 'https://api.vize.ai/v2/classify/'
        headers = {
            'Authorization': "Token ee353c77a1d0b5fdde2a2520d7f142ae6193e370",
            'Content-Type': 'application/json'
        }
        with open(self.run_image_directory, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

        data = {
            'task_id': 'e7011970-c1e5-4935-a3ab-1488f41c55e4',
            'records': [{"_base64": encoded_string}]
        }

        response = requests.post(url, headers=headers, data=json.dumps(data))
        json_obj = json.loads(response.text)
        result = json_obj['records'][0]['best_label']['name']
        self.mirto.set_lcd_message(result, 0)
        print(result)
        return json_obj['records'][0]['best_label']['name']

    # TODO this needs to be reviewed when Opencv installation comes back
    def what_sign(self):
        """
        Checks what sign does the camera see from a VIDEOSTREAM
        :return:
        """
        # initialize the video stream and allow the camera sensor to warm up
        vs = VideoStream(src=1).start()
        # vs = VideoStream(usePiCamera=True).start()

        # grab the frame from the threaded video stream and resize it to
        # have a maximum width of 400 pixels
        frame = vs.read()
        frame = imutils.resize(frame, width=400)

        # find the barcodes in the frame and decode each of the barcodes
        barcodes = pyzbar.decode(frame)
        # loop over the detected barcodes
        for barcode in barcodes:
            barcodeData = barcode.data.decode("utf-8")
            print(barcodeData)
            # close the output CSV file do a bit of cleanup
            print("[INFO] cleaning up...")
            cv2.destroyAllWindows()
            vs.stop()

    def main_loop(self):
            while True:
                try:
                    colour = self.what_color_is()
                    if colour == "GREEN":
                        print("Image recognised green traffic light")
                        self.mirto.set_lcd_message("IT's GREEN, move ... ", 1)
                        self.mirto.set_motors_rpm(20, 20, 10000)
                    elif colour == "RED":
                        print("Image recognised red traffic light")
                        self.mirto.set_lcd_message("IT's RED, stop ... ", 1)
                        self.mirto.stop_motors()

                except KeyboardInterrupt:
                    print('Interrupted')
                    try:
                        sys.exit(0)
                    except SystemExit:
                        sys.exit(0)

    def drive_for(self, millisec):
        """
        Function to make robot drive for a certain amount of millimeters
        :param mm: int
        :return:
        """
        self.mirto.set_motors_rpm(50, 50, millisec)
        print("driving straight for %s millisec" % millisec)


# trainer = TrainDetector()
trafficLight = TrafficLightDetector()
trafficLight.what_color_is()
# driveFor(3000)
