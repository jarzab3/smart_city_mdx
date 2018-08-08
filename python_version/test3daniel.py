import requests
import json
import base64
#import imutils
#import cv2
import os
import json
import sys
from python_asip_client.serial_mirto_robot import SerialMirtoRobot
from python_asip_client.mirto_robot import MirtoRobot
import picamera
from picamera import PiCamera
import logging
from time import sleep
from python_asip_client.serial_mirto_robot import SerialMirtoRobot
from python_asip_client.mirto_robot import MirtoRobot


services = SerialMirtoRobot()
services = services.get_services()
mirto = MirtoRobot(services)

# logging.getLogger("requests").setLevel(logging.WARNING)
# logging.getLogger("urllib3").setLevel(logging.WARNING)
# logging.getLogger("").setLevel(logging.WARNING)
# camera = picamera.PiCamera()



# Run services test
camera = PiCamera()


def whatColoris():
    """
    Tells the colour of the traffic light
    :return:
    """
    sleep(0.5)
    camera.capture('/home/smart1/capture5.jpg')
    print("Picutre taken ..... ")
    url = 'https://api.vize.ai/v2/classify/'
    headers = {
        'Authorization': "Token c69c02e60580424a268d03effadec9f404938c7e",
        'Content-Type': 'application/json'
    }
    with open("/home/smart1/capture5.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')

    data = {
        'task_id': '71aa86cb-0198-4229-87e5-1f667ade00f2',
        'records': [{"_base64": encoded_string}]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    json_obj = json.loads(response.text)
    return json_obj['records'][0]['best_label']['name']


def whatSign():
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

def main():
        while True:
            try:
                colour = whatColoris()
                if (colour == "GREEN-TrafficLight"):
                    print("GO")
                    mirto.set_motors_rpm(20, 20, 10000)
                elif (colour == "RED-TrafficLight"):
                    print("STOP")
                    mirto.stop_motors()

            except KeyboardInterrupt:
                print('Interrupted')
                try:
                    sys.exit(0)
                except SystemExit:
                    os._exit(0)

def takePics(n):
    """
    Takes a certain n amount of pictures in order to provide pictures to train the AI
    :param n: int
    :return:
    """
    while True:
        try:
            for x in range(0, n):
                sleep(0.5)
                camera.capture('/home/smart1/images/capture_%s.jpg' % x)
                sleep(1)
                print("DONE: Picuture%s" % x)
            break
        except KeyboardInterrupt:
            print('Interrupted')
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)

def driveFor(ss):
    """
    Function to make robot drive for a certain amount of millimeters
    :param mm: int
    :return:
    """
    mirto.set_motors_rpm(50,50,ss)
    print("driving straight for %s millisec" %ss)



driveFor(3000)
