from time import sleep
from asip.serial_mirto_robot import SerialMirtoRobot
robot = SerialMirtoRobot()

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
    # So this will give you an array of True (if on black) False (if on White) and 0 (if nothing)
    ir_order = [0, 2, 1]

    for i in ir_order:
        values.append(robot.get_ir(i))

    return values

def getSensorReadings():
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
    # So this will give you an array of True (if on black) False (if on White) and 0 (if nothing)
    ir_order = [0, 2, 1]

    for i in ir_order:

        tempValue = robot.get_ir(i)

        threshold = 500

        if tempValue > threshold:
            values.append(True)
        else:
            values.append(False)

    return values

def forward():
    robot.set_motors(50, 50)

def backwards():
    robot.set_motors(-100, -100)

def left():
    robot.set_motors(30, 0)

def right():
    robot.set_motors(0, 30)

def brake():
    robot.stop_motors()

try:
    while True:
        all_values = getSensorReadings()

        left_sensor = all_values[0]
        center_sensor = all_values[1]
        right_sensor = all_values[2]

        values = read_all_ir_values()

        print (all_values)


        print("Values from IR: %s" % values)

        # if left_sensor:
        #     right()
        #
        # if right_sensor:
        #     left()
        #
        # else:
        #     forward()

        sleep(0.2)


except Exception as error:
    print (error)