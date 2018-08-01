from time import sleep
from asip.serial_mirto_robot import SerialMirtoRobot

robot = SerialMirtoRobot()

robot.clear_LCD()
robot.set_LCD_message("robot test", 1)
robot.set_LCD_message("1, 2, 3...", 2)
robot.set_LCD_message("All Good!", 3)


robot.set_motors(88, 88)
