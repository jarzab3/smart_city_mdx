# Author: Noman Niazi
#Code may not be used by third part individuals or groups
from mirto_asip_manager.mirto_robot import MirtoRobot
from time import sleep
import time


services_to_run = {"encoders": [True, False], "motors": [True, False], "ir_sensors": [True, False],
                   "tone": [True, False]}


# Run services test
mirto = MirtoRobot(debug=True, services_on=services_to_run)

from time import sleep

def get_Motor_Distance_Values():

    motor_Distance = []

    enc = mirto.get_encoders_values()
    OneEncMM = 2 * 3.14 * (66.20 / 2) / 1632 / 10
    l_OneEncMM = (enc[0] * OneEncMM)
    r_OneEncMM = (enc[1] * OneEncMM * -1)

    motor_Distance.extend((l_OneEncMM, r_OneEncMM))

    return motor_Distance

while True:
    all_motor_Distance = get_Motor_Distance_Values()

    lM_Dtnc = all_motor_Distance[0]
    rM_Dtnc = all_motor_Distance[1]

    print("Motor Distance: %s" %all_motor_Distance)

    if lM_Dtnc < rM_Dtnc:
        mirto.set_motors(4,0)
    elif rM_Dtnc < lM_Dtnc:
        mirto.set_motors(0,4)
    else:
        mirto.stop_motors()
        print("....................Reset..Complete....................")
        sleep(0.01)

        break
