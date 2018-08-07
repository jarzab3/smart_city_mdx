from mirto_asip_manager.mirto_robot import MirtoRobot
from time import sleep
services_to_run = {"encoders": [True, False], "motors": [True, False], "ir_sensors": [True, False]}
# Run services test
mirto = MirtoRobot(debug=False, services_on=services_to_run)
# mirto.set_motors(100,0)
# sleep(1)
# mirto.stop_motors()
# mirto.terminate()
#  get_encoders_values',
#  'get_ir_sensors_values',
#  'get_left_encoder_values',
#  'get_right_encoder_values',
#  'get_version_info',
#  'robot',
#  'set_motors',
#  'stop_motors',
#  'terminate',
#  'test_encoders',
#  'test_ir_sensors',
#  'test_motor']
# mirto.test_ir_sensors()

print()
rightIR = 0;
leftIR = 0;
middleIR = 0;
try:
    while True:

        # Getting sensor values
        rightIR = mirto.get_ir_sensors_values()[1]
        middleIR = mirto.get_ir_sensors_values()[2]
        leftIR = mirto.get_ir_sensors_values()[0]
        #  Printing the values
        print("RIGHT SENSOR = " + str(rightIR))
        print("LEFT SENSOR = " + str(leftIR))
        print("MIDDLE SENSOR = " + str(middleIR))
        sleep(0.05)
        if(leftIR > 100):
            mirto.set_motors(40, 20)
            if(rightIR > 100):
                mirto.set_motors(20, 40)
            else:
                mirto.set_motors(20, 20)
        # else:
        #     mirto.set_motors(0, 0)




except KeyboardInterrupt:

    print("Process terminated ")

    mirto.stop_motors()
    mirto.terminate()
    pass