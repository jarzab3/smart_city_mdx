from python_asip_client.tcp_mirto_robot import TCPMirtoRobot
from python_asip_client.serial_mirto_robot import SerialMirtoRobot
import sys


class MirtoRobot:
    def __init__(self, _services):
        self.motors = _services.get("motors")
        self.irs = _services.get('irs')
        self.bumps = _services.get('bumps')
        self.pid = _services.get('pid')

    # Setting the two motors speed
    def set_motors(self, s0, s1):
        self.motors[0].set_motor(s0)
        self.motors[1].set_motor(s1)
        sys.stdout.write("DEBUG: setting motors to {}, {}\n".format(s0, s1))

    # Stopping the two motors
    def stop_motors(self):
        self.motors[0].stop_motor()
        self.motors[1].stop_motor()

    # Retrieving data from IR sensor, -1 if sensor number is wrong
    def get_ir(self, sensor):
        return self.irs[sensor].get_ir() if sensor in [0, 1, 2] else -1

    # Retrieving count value from encoder sensor, -1 if sensor number is wrong
    def get_count(self, sensor):
        return self.motors[sensor].get_count() if sensor in [0, 1] else -1

    # Retrieving count value from bump sensor, -1 if sensor number is wrong
    def is_pressed(self, sensor):
        return self.bumps[sensor].is_pressed() if sensor in [0, 1] else -1

    def reset_count(self):
        self.motors[0].reset_count()
        sys.stdout.write("Reset encoders\n")

    def get_all_ir_values(self, sensor_order=None):
        """
        This function is getting IR sensor values and return a list with those results.
        Some robots have ir sensors in different order, hence as a parameter it can take a list with a order of sensors.
        :param sensor_order:
        :return: sensor values: list
        """
        if sensor_order is None:
            sensor_order = [0, 1, 2]
        sensor_values = []
        for sensor in sensor_order:
            sensor_values.append(self.get_ir(sensor))
        return sensor_values

    def set_Motor_RPM(self, motor_ID, RPM, duration):
        self.pid[0].set_Motor_RPM(motor_ID,RPM,duration)
    def set_Motors_RPM(self,  RPM0, RPM1, duration):
        self.pid[0].set_Motors_RPM(RPM0,RPM1,duration)

if __name__ == '__main__':
    # services = SerialMirtoRobot()
    ip_address = "10.14.122.61"
    services = TCPMirtoRobot(ip_address, 9999).get_services()
    mirto_robot = MirtoRobot(services)
