from mirto_asip_manager.mirto_robot import MirtoRobot
from time import sleep


services_to_run = {"encoders": [True, False], "motors": [True, False], "ir_sensors": [True, False],
                   "tone": [True, False]}


# Run services test
mirto = MirtoRobot(debug=True, services_on=services_to_run)

from time import sleep


while True:
    enc = mirto.get_encoders_values()
    Distance = 2 * 3.14 * (66.20 / 2) / 1632 / 10
    print(enc[0] * Distance)
    print(enc[0] * Distance)
    sleep(0.1)
