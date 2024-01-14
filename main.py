from robot import Robot
import time


def step1_move3s(robot: Robot):
    robot.setMotorsSpeed(0.2, 0.2)
    time.sleep(1.0)
    robot.setMotorsSpeed(0.0, 0.0)


def step2_turn3s(robot: Robot):
    # TODO step2
    pass


def step3(robot: Robot):
    # TODO step3
    pass


def step4(robot: Robot):
    # TODO step4
    pass


def step5(robot: Robot):
    # TODO step5
    pass


def step6(robot: Robot):
    # TODO step6
    pass


if __name__ == '__main__':
    # Create robot and wait is ready
    robot = Robot("127.0.0.1", 6543)
    robot.waitReady()
    print("Lancement du programme")

    step1_move3s(robot)
    #step2_turn3s(robot)
    #step3(robot)
    #step4(robot)
    #step5(robot)
    #step6(robot)

    # Exit
    print("Fin du programme")
    robot.close()
