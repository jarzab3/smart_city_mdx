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


def turnrobot(degrees, speed, direction=True):
    encoderVal = get_Motor_Distance_Values()
    lM_Dtnc = encoderVal[0]
    # encoderVal = get_Motor_Distance_Values()
    lM_Dtnc = encoderVal[0]
    # rM_Dtnc = encoderVal [1]

    # Diameter of wheels in mm
    # wheelDiameter = 66.20
    # Encoder values for one full revolution of the wheel
    # oneRevolution = 1632
    # Space  between wheels
    wheelsSpacing = 158

    circumferenceOfCircle = 2 * 3.14 * (wheelsSpacing / 2)
    oneWheelDistance = (circumferenceOfCircle / 360) * degrees

    while lM_Dtnc <= oneWheelDistance:
        encoderVal = get_Motor_Distance_Values()
        lM_Dtnc = encoderVal[0]
        mirto.set_motors(speed, 0)

    else:
        mirto.stop_motors()


def drive_for(mm):
    print("Start program")
    all_motor_Distance = get_Motor_Distance_Values()
    lM_Dtnc = all_motor_Distance[0]
    rM_Dtnc = all_motor_Distance[1]
    right_power = 30
    left_power = 30

    while True:
        if lM_Dtnc < mm:
            left_power = 30
        else:
            left_power = 0

        if rM_Dtnc < mm:
            right_power = 30
        else:
            right_power = 0

        all_motor_Distance = get_Motor_Distance_Values()
        lM_Dtnc = all_motor_Distance[0]
        rM_Dtnc = all_motor_Distance[1]

        mirto.set_motors(left_power, right_power)
        print("Motor distances: %s" % [lM_Dtnc, rM_Dtnc])
        if right_power == 0 and left_power ==0:
            break

    else:
        mirto.stop_motors()
        print("Reached destination")

# drive_for(mm=500)
turnrobot(90, 30)