from mirto_asip_manager import MirtoRobot

enabled_services = {"encoders": [True, False]}
# Run services test
mirto = MirtoRobot(enabled_services)
mirto.get_version_info()
mirto.test_encoders(0.1, 2)
mirto.test_motor(True, 3)
mirto.test_ir_sensors(5, 0.2)
# This will stop all threads and close ports
mirto.terminate()

