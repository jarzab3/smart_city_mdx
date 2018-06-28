from asip_manager import AsipManager
from time import sleep

class MirtoRobot:
    def __init__(self):
        self.robot = AsipManager()
        self.robot.initialize_main()

    def terminate(self):
        self.robot.terminate_all()

    def get_left_encoder_values(self, delta=False):
        # Access encoders service
        encoders = self.robot.all_services.get('encoders')
        # Get values
        left_values_all = encoders.left_values
        if delta:
            return left_values_all
        else:
            return left_values_all[1]

    def get_right_encoder_values(self, delta=False):
        # Access encoders service
        encoders = self.robot.all_services.get('encoders')
        # Get values
        right_values_all = encoders.right_values
        if delta:
            return right_values_all
        else:
            return right_values_all[1]

    def set_motors(self, speed0, speed1):
        motor_1 = self.robot.all_services.get('motor_1')
        motor_2 = self.robot.all_services.get('motor_2')
        motor_1.set_motor(speed0)
        motor_2.set_motor(speed1)
        print("DEBUG: setting motors speed to: {}, {}".format(speed0, speed1))

    def stop_motors(self):
        motor_1 = self.robot.all_services.get('motor_1')
        motor_1.stop_motor()

    def test(self):
        try:
            while True:
                print(self.get_left_encoder_values(), self.get_right_encoder_values())
                sleep(0.1)
        except KeyboardInterrupt:
            self.robot.terminate_all()
            print ("Finish test")

    def motor_test(self):
        self.set_motors(90, 30)
        sleep(5)
        self.stop_motors()

if __name__ == '__main__':
    mirto = MirtoRobot()
    # mirto.test()
    mirto.motor_test()
    mirto.terminate()

