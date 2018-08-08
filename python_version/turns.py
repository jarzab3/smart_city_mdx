# Author: Noman Niazi
#Code may not be used by third part individuals or groups
from mirto_asip_manager.mirto_robot import MirtoRobot
from time import sleep

services_to_run = {"encoders": [True, False], "motors": [True, False], "ir_sensors": [True, False],
                   "tone": [True, False]}

# Run services test
mirto = MirtoRobot(debug=False, services_on=services_to_run)


def get_Motor_Distance_Values():
    motor_Distance = []
    enc = mirto.get_encoders_values()
    OneEncMM = 2 * 3.14 * (66.20 / 2) / 1632 / 10
    l_OneEncMM = (enc[0] * OneEncMM)
    r_OneEncMM = (enc[1] * OneEncMM * -1)


    motor_Distance.extend((l_OneEncMM, r_OneEncMM))

    return motor_Distance

def drive_for():
    print("Start program")
    all_motor_Distance = get_Motor_Distance_Values()
    lM_Dtnc = all_motor_Distance[0]
    rM_Dtnc = all_motor_Distance[1]
    right_power = 30
    left_power = -30


    while True:

        if rM_Dtnc < 12 and lM_Dtnc > -12:
            right_power = 30
            left_power = -30

        else:
            right_power = 0
            left_power = 0


        all_motor_Distance = get_Motor_Distance_Values()
        lM_Dtnc = all_motor_Distance[0]
        rM_Dtnc = all_motor_Distance[1]

        mirto.set_motors(left_power, right_power)
        print("Motor distances: %s" % [lM_Dtnc, rM_Dtnc])
        if right_power == 0 and left_power == 0:
            break

    mirto.stop_motors()
    sleep(2)

    while True:

        if rM_Dtnc < 50 and lM_Dtnc > -50:
            right_power = 30
            left_power = -30

        else:
            right_power = 0
            left_power = 0


        all_motor_Distance = get_Motor_Distance_Values()
        lM_Dtnc = all_motor_Distance[0]
        rM_Dtnc = all_motor_Distance[1]

        mirto.set_motors(left_power, right_power)
        print("Motor distances: %s" % [lM_Dtnc, rM_Dtnc])
        if right_power == 0 and left_power == 0:
            break
    else:
        mirto.stop_motors()
        print("All turns complete")

drive_for()
