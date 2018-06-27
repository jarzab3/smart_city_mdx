#!/usr/bin/env python
import time
import serial
import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-p", "--port", required=True,
                    help="Serial port to listen")

args = vars(ap.parse_args())

port = args["port"]

serialport = serial.Serial(port, 57600, timeout=0.5)

while True:
    # command = serialport.read()

    command = serialport.readline()

    print(str(command))