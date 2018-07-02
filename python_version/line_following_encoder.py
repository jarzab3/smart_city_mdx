# importing library
from time import sleep
from asip.serial_mirto_robot import SerialMirtoRobot

robot = SerialMirtoRobot()

def read_count():
    """
    This function is reading values for all ir sensors.
    example
    # :param i:
    # :type i: int
    end of example
    :return: Count Sensor values
    :rtype: array
    """
    robot.set_motors(100,100)

    count_values = []

    # Range stands for all sensors.
    # 0 is left, 1 is center and 2 is right
    for i in range(0, 2):
        count_values.append(robot.get_count(i))

    return count_values


while True:
    count_values = read_count()

    print("Values from count: %s" %count_values)

    sleep(0.3)
