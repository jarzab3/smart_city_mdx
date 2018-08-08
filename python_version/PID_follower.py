from mirto_asip_manager.mirto_robot import MirtoRobot
from time import sleep


class DrivingRobot:
    def __init__(self):
        self.services_to_run = {"encoders": [True, False], "motors": [True, False], "ir_sensors": [True, False],
                           "tone": [True, False]}

        # Init services
        self.mirto = MirtoRobot(debug=False, services_on=self.services_to_run)


    def get_mirto_ir_values(self):
        ordered_ir_values = []
        ir_values = mirto.get_ir_sensors_values()
        left_ir = ir_values[0]
        center_ir = ir_values[2]
        right_ir = ir_values[1]
        ordered_ir_values.extend((left_ir, center_ir, right_ir))
        return ordered_ir_values


    def get_ir_values_threshold(self):
        """

        :return:
        """
        ir_values = self.mirto.get_ir_sensors_values()
        sensors_vals = {"left": [ir_values[0], False], "center": [ir_values[2], False], "right": [ir_values[1], False]}
        threshold = 110
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
                return ir_values_after_check
                if ir_values_after_check.get("left")[1]:
                    self.mirto.set_motors(20, 40)
                elif ir_values_after_check.get("right"[1]):
                   self.mirto.set_motors(40, 20)
                else:
                    self.mirto.set_motors(35, 35)
                sleep(0.1)
        except Exception as error:
            print (error)

drive = DrivingRobot()
drive.run_main()
