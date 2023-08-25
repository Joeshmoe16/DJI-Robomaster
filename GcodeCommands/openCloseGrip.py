import time
import math

# For robomaster control
import robomaster
from robomaster import robot

def openGrip():
    ep_gripper.open(power=50)
    time.sleep(1.5)
    ep_gripper.pause()


def closeGrip():
    ep_gripper.close(power=80)
    time.sleep(1.5)
    ep_gripper.pause()

# set up robot
ep_robot = robot.Robot()
ep_robot.initialize(conn_type="ap")

ep_gripper = ep_robot.gripper

openGrip()

time.sleep(2)

closeGrip()
