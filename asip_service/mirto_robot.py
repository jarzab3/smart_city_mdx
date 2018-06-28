from asip_manager import AsipManager
from time import sleep
from settings import logging as log
import time


class MirtoRobot:
    def __init__(self):
        self.robot = AsipManager()
        self.robot.initialize_main()

    def terminate(self) -> None:
        """
        Function which is making all threads and ports terminated
        :return:
        """
        self.robot.terminate_all()

    def get_left_encoder_values(self, delta: bool=False) -> list:
        # Access encoders service
        encoders = self.robot.all_services.get('encoders')
        # Get values
        left_values_all = encoders.left_values
        if delta:
            return left_values_all
        else:
            return left_values_all[1]

    def get_right_encoder_values(self, delta: bool=False) -> list:
        # Access encoders service
        encoders = self.robot.all_services.get('encoders')
        # Get values
        right_values_all = encoders.right_values
        if delta:
            return right_values_all
        else:
            return right_values_all[1]

    def set_motors(self, speed0: int, speed1: int) -> None:
        motor_1 = self.robot.all_services.get('motor_1')
        motor_2 = self.robot.all_services.get('motor_2')
        motor_1.set_motor(speed0)
        motor_2.set_motor(speed1)
        log.info("Setting motor: '{}': {} motor:'{}': {}".format(motor_1.name, speed0, motor_2.name, speed1))

    def stop_motors(self) -> None:
        motor_1 = self.robot.all_services.get('motor_1')
        motor_2 = self.robot.all_services.get('motor_1')
        motor_1.stop_motor()
        motor_2.stop_motor()

    def test_encoders(self, interval: float=0.1, time_to_finish: int=10) -> None:
        end_time = time.time() + time_to_finish
        while time.time() < end_time:
            print(self.get_left_encoder_values(True), self.get_right_encoder_values(True))
            sleep(interval)
        log.info("Finish encoder test")

    def test_motor(self) -> None:
        self.set_motors(30, 0)
        sleep(5)
        self.stop_motors()


if __name__ == '__main__':
    mirto = MirtoRobot()
    mirto.test_encoders(0.1, 2)
    mirto.test_motor()
    # This will stop all threads and close ports
    mirto.terminate()

