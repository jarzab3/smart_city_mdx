from asip_service.mirto_robot import MirtoRobot

def test1():
    mirto = MirtoRobot()
    mirto.test_encoders(0.1, 7)


test1()