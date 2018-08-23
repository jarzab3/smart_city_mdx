# --AUTHOR: Mr Noman Niazi--
# --copyright: = Copyright 2018, Middlesex University--
# --license: MIT License--
# --maintainer: "Mr Noman Niazi--
from python_asip_client.tcp_mirto_robot import TCPMirtoRobot
from python_asip_client.mirto_robot import MirtoRobot
from time import sleep


class RobotMain:
    def __init__(self):
        services = TCPMirtoRobot("robot1").get_services()
        self.mirto = MirtoRobot(services)

    def get_mirto_ir_values(self):
        ordered_ir_values = []
        ir_values = self.mirto.get_all_ir_values()
        left_ir = ir_values[0]
        center_ir = ir_values[2]
        right_ir = ir_values[1]
        ordered_ir_values.extend((left_ir, center_ir, right_ir))
        return ordered_ir_values

    def get_ir_values_threshold(self):
        """
        This function compares the ir values with the threshold value retrieved from when ir is placed on black surface.
        :return:
        """
        ir_values = self.mirto.get_all_ir_values()
        sensors_vals = {"left": [ir_values[0], False], "center": [ir_values[2], False], "right": [ir_values[1], False]}
        threshold = 250
        for sensor in sensors_vals.keys():
            sensor_val = sensors_vals.get(sensor)
            sensors_vals.update(sensors_vals)
            if sensor_val[0] > threshold:
                sensor_val[1] = True
                sensors_vals[sensor] = sensor_val
            else:
                sensor_val[1] = False
                sensors_vals[sensor] = sensor_val
        # print(sensors_vals, "\n")
        return sensors_vals

    def run_main(self):
        try:
            while True:
                ir_values_after_check = self.get_ir_values_threshold()
                if ir_values_after_check.get("left")[1]:
                    # self.mirto.set_motors_rpm()
                    self.mirto.set_motors(19, 25)
                elif ir_values_after_check.get("right")[1]:
                    self.mirto.set_motors(25, 19)
                elif ir_values_after_check.get("center")[0]:
                   self.mirto.set_motors(-24, 24)
                # elif ir_values_after_check.get("center")[0] and ir_values_after_check.get("right")[0]:
                #     mirto.set_motors(-50,50)
                # elif ir_values_after_check.get("center")[0] and ir_values_after_check.get("left")[0]:
                #     mirto.set_motors(50,-50)
                else:
                    self.mirto.set_motors(24, 24)
                sleep(0.05)
        except Exception as error:
            print(error)


drive = RobotMain()
drive.run_main()
    # l = 43 c = 39 r = 92
    # l = 885 c = 898 r = 896
    # l = between 60 and 140
    # c = between and
    # r = between 90 and 300
