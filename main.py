from robot import Robot
import time


def simpleMove(robot: Robot):
    # Turn to right a little
    robot.setMotorSpeed(Robot.MotorIndex.LEFT, 0.1)
    robot.setMotorSpeed(Robot.MotorIndex.RIGHT, -0.1)
    time.sleep(1.0)
    robot.setMotorSpeed(Robot.MotorIndex.LEFT, 0.0)
    robot.setMotorSpeed(Robot.MotorIndex.RIGHT, 0.0)
    time.sleep(1.0)

    # Go straight up to detect line track or timeout 1 second
    robot.setMotorsSpeed(0.5, 0.5)
    robot.waitChanged(Robot.EventType.LINE_TRACK_IS_DETECTED, 1.0)
    robot.setMotorsSpeed(0.0, 0.0)


def lineTrack(robot: Robot):
    # Follow line track
    robot.setMotorsSpeed(0.3, 0.3)
    while True:
        robot.waitChanged(Robot.EventType.LINE_TRACK_IS_DETECTED)
        if robot.getLineTracksIsDetected(0):
            robot.setMotorsSpeed(0.4, 0.2)
        else:
            robot.setMotorsSpeed(0.2, 0.4)


if __name__ == '__main__':
    # Create robot and wait is ready
    robot = Robot("127.0.0.1", 6543)
    robot.waitReady()

    lineTrack(robot)

    # Exit
    robot.close()
