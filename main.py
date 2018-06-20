#!/usr/bin/env python

from time import sleep
from python_asip.python_asip_client.mirto_robot_classes.serial_mirto_robot import SerialMirtoRobot

robot = SerialMirtoRobot()

robot.clear_LCD()
robot.set_LCD_message("robot test", 1)
robot.set_LCD_message("1, 2, 3...", 2)
robot.set_LCD_message("ami working?", 3)
robot.set_motors(100, 100)
sleep(2)
robot.stop_motors()
