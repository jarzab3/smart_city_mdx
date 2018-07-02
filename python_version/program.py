from time import sleep
from asip.serial_mirto_robot import SerialMirtoRobot

robot = SerialMirtoRobot()

# robot.clear_LCD()
# robot.set_LCD_message("robot test", 1)
# robot.set_LCD_message("1, 2, 3...", 2)
# robot.set_LCD_message("ami working?", 3)
# robot.set_motors(100, 100)
# sleep(2)
# robot.stop_motors()


def read_all_ir_values():
    """
    This function is reading values for all ir sensors.

    example
    # :param i:
    # :type i: int
    end of example
    :return: IR Sensor values
    :rtype: array
    """
    values = []

    # Range stands for all sensors.
    # 0 is left, 1 is center and 2 is right
    for i in range(0, 3):
        values.append(robot.get_ir(i))

    return values


while True:
    values = read_all_ir_values()

    print("Values from IR: %s" %values)

    sleep(0.3)
