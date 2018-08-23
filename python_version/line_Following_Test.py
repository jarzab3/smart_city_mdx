# Author: Noman Niazi
#Code may not be used by third part individuals or groups
from python_asip_client.serial_mirto_robot import SerialMirtoRobot
from python_asip_client.mirto_robot import MirtoRobot
from time import sleep
services = SerialMirtoRobot()
services = services.get_services()
robot = MirtoRobot(services)

# creating a function call read_all_ir_values that reads the values from the ir sensors on the mirto robot
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
    # variable called values that will hold an array
    values = []

    # range stands for all sensors.
    # 0 is left, 2 is center and 1 is right
    ir_order = [0, 2, 1]

    # for loop
    for i in ir_order:
        # takes each reading and then adds each reading for example ir 0 = 345, ir 2 = 532, ir 1 = 684 into array called value which will give you [345, 532, 684]
        values.append(robot.get_ir(i))
    # returns the array with each ir value
    return values

# creating a function call read_all_ir_values that retreive the values from each individual ir sensor. similar to the top one but returns true if ir on black surface
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
    # variable called values that will hold an array
    values = []

    # 0 is left, 1 is center and 2 is right

    ir_order = [0, 2, 1]

    # so this will give you an array of True (if on black) False (if on White) and 0 (if nothing)
    for i in ir_order:

        tempValue = robot.get_ir(i)
        # variable called threshold which is equalled to 500. this is the value that we compare each ir value to e.g. if ir value > 500 then do this....
        threshold = 300
        # we take the ir reading and say if it is greater than our threshold which is 500
        if tempValue > threshold:
            # if ir value is greater than the threshold add True to that ir number in the array e.g. if the ir 0 value is higher than 500, it will put true it the array like [True, ir 2, 1]]
            values.append(True)
        else:
            # if the ir value is not greater than 500, add False to that ir position in the array e.g. [ir 0, False, ir 1]
            values.append(False)
    # returns the complete array
    return values

# define function called forward. movies robot forward
def forward():
    robot.set_motors(85, 96)

# define function called backwards. movies robot backwards
def backwards():
    robot.set_motors(-85, -96)

# define function called left. movies robot left
def left():
    robot.set_motors(98, 20)

# define function called right. movies robot right
def right():
    robot.set_motors(20, 99)

# define function called brake. movies robot brake
def brake():
    robot.stop_motors()

# try is used for error handeling. for example we say try: this loop, if the loop is true, then continue to execute that loopself however
# if at a certain point in the loop, a false result is evaluated from a line of code then print "error". the "error" print is shown at the bottom.
try:

    # a while loop
    while True:
        all_values = getSensorReadings()

        left_sensor = all_values[0]
        center_sensor = all_values[1]
        right_sensor = all_values[2]

        values = read_all_ir_values()

        print (all_values)


        print("Values from IR: %s" % values)

        if left_sensor:
             left()
        elif right_sensor:
             right()
        else:
             forward()


        # print arrays every 0.2 seconds the quicker it prints, the more precise the ir values are
        sleep(0.01)


except Exception as error:
    print (error)
