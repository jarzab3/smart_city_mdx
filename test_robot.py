from mirto_asip_manager.mirto_robot import MirtoRobot

services_to_run = {"encoders": [True, False], "motors": [True, False], "ir_sensors": [True, False]}
# Run services test
mirto = MirtoRobot(debug=False, services_on=services_to_run)
mirto.test_encoders(0.1, 5)
mirto.test_motor(True, 10)
mirto.test_ir_sensors(5, 0.2)
# This will stop all threads and close ports
mirto.terminate()