# importing library
from time import sleep
import requests
import cv2
import json
from asip.serial_mirto_robot import SerialMirtoRobot
robot = SerialMirtoRobot()

def  readTrafficLight():

    cap = cv2.VideoCapture(1)

    while (True):
        ret, frame = cap.read()
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)

        cv2.imshow('frame', rgb)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            out = cv2.imwrite('capture.jpg', frame)
            break

    cap.release()
    cv2.destroyAllWindows()


    url = 'https://api.vize.ai/v1/classify/'
    headers = {'Authorization': "Token c69c02e60580424a268d03effadec9f404938c7e"}
    files = {'image_file': open('capture.jpg', 'rb')}
    data = {'task': '2e876821-ab66-4e91-bf42-b9a3befa6d79'}

    response = requests.post(url, headers=headers, files=files, data=data)
    if response.raise_for_status():
        json_obj = json.loads(response.text)
        print(json_obj['best_label']['label_name'])  # prints the string with 'source_name' key
    else:
        print('Error posting API: ' + response.text)








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