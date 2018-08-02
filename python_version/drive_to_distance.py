# Author: Noman Niazi
#Code may not be used by third part individuals or groups
import threading
import requests
import argparse
import datetime
import imutils
import time
import cv2

import json
from mirto_asip_manager.mirto_robot import MirtoRobot
from time import sleep
from threading import Thread

# from pyzbar import pyzbar

services_to_run = {"encoders": [True, False], "motors": [True, False], "ir_sensors": [True, False],
                   "tone": [True, False]}

# Run services test
mirto = MirtoRobot(debug=False, services_on=services_to_run)


def whatColoris():
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

    # cv2.imshow('frame', rgb)

    out = cv2.imwrite('capture.jpg', frame)

    cap.release()
    cv2.destroyAllWindows()
    import requests

    url = 'https://api.vize.ai/v1/classify/'
    headers = {'Authorization': "Token c69c02e60580424a268d03effadec9f404938c7e"}
    files = {'image_file': open('capture.jpg', 'rb')}
    data = {'task': '71aa86cb-0198-4229-87e5-1f667ade00f2'}

    response = requests.post(url, headers=headers, files=files, data=data)

    cap = cv2.VideoCapture(1)
    if response.raise_for_status():
        return(response.text)


def get_motor_distance_values():
    motor_Distance = []
    enc = mirto.get_encoders_values()
    OneEncMM = 2 * 3.14 * (66.20 / 2) / 1632 / 10
    l_OneEncMM = (enc[0] * OneEncMM)
    r_OneEncMM = (enc[1] * OneEncMM * -1)


    motor_Distance.extend((l_OneEncMM, r_OneEncMM))

    return motor_Distance

def get_mirto_ir_values():
    ordered_ir_values = []
    ir_values = mirto.get_ir_sensors_values()
    left_ir = ir_values[0]
    center_ir = ir_values[2]
    right_ir = ir_values[1]
    ordered_ir_values.extend((left_ir, center_ir, right_ir))
    return ordered_ir_values

def get_ir_values_threshold():

    ir_values = mirto.get_ir_sensors_values()
    sensors_vals = {"left": [ir_values[0], False], "center": [ir_values[2], False], "right": [ir_values[1], False]}
    threshold = 700
    for sensor in sensors_vals.keys():
        sensor_val = sensors_vals.get(sensor)
        sensors_vals.update(sensors_vals)
        if sensor_val[0] > threshold:
            sensor_val[1] = True
            sensors_vals[sensor] = sensor_val
        else:
            sensor_val[1] = False
            sensors_vals[sensor] = sensor_val
    print(sensors_vals, "\n")
    return sensors_vals



def drive_for(mm):
    print("Start program")
    all_motor_Distance = get_motor_distance_values()
    lM_Dtnc = all_motor_Distance[0]
    rM_Dtnc = all_motor_Distance[1]

    while True:
        ir_values_after_check = get_ir_values_threshold()
        if lM_Dtnc < mm and rM_Dtnc < mm and ir_values_after_check.get("left")[1]:
            mirto.set_motors(10, 30)
        elif rM_Dtnc < mm and rM_Dtnc < mm and ir_values_after_check.get("right")[1]:
            mirto.set_motors(30, 10)
        elif rM_Dtnc < mm and rM_Dtnc < mm and ir_values_after_check.get("center")[1]:
            mirto.set_motors(45, 45)

        all_motor_Distance = get_motor_distance_values()
        lM_Dtnc = all_motor_Distance[0]
        rM_Dtnc = all_motor_Distance[1]

        print("Motor distances: %s" % [lM_Dtnc, rM_Dtnc])
        if lM_Dtnc > mm and rM_Dtnc > mm:
            mirto.stop_motors()
            return
        else:
            mirto.stop_motors()
            print("Reached destination")
drive_for(mm=25)
