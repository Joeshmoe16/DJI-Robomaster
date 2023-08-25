import time

#For robomaster control
import robomaster
from robomaster import robot

#////////////////////global Variable definitions//////////////////
#these are all for basic motion
X_VAL = 0.5
Y_VAL = 0.6
Z_VAL = 90

CUR_X = 0
CUR_Y = 0
CUR_Z = 3
CUR_R = 0

SCALE = 100
SIMPLE_SPEED = 1
SIMPLE_TURN_SPEED = 45

#////////////////////////////////Main/////////////////////////////////////////////
def main():
    #open file and read line by line

    with open("star.txt", "r") as gcodeFile:
        #repeats until end of file is reached (or error is thrown)
        i = 1
        while(True):
            #reads the current line and puts it in a string.
            command = gcodeFile.readline()

            #prints out and then indexes the current line in the file. Only Prints
            #if G0 command is being run.
            if "G0" in command:
                print()
                print(i)
            i += 1

            #Sends a line to be executed. If no relevant command is found the loop simply repeats.
            execute(command)

            #exits the while loop when the end of the gcode is reached
            if "(end)" in command:
                break

#//////////////////execute: decides which command///////////////////
def execute(command):
    if "G00" in command:
        print(command)
        x, y, z, f = get_values(command)
        G00_G01(x, y, z)

    elif "G01" in command:
        print(command)
        x, y, z, f = get_values(command)
        G00_G01(x, y, z)

    elif "G02" in command:
        print(command)

    elif "G03" in command:
        print(command)


#/////////////////G00 and G01 Helper Function////////////////
def G00_G01(x, y, z):
    #moves chalk down if neg. z or up if pos. z
    global CUR_Z
    if z != 4000:
        if z < 0 and CUR_Z != 1:
            print(CUR_Z)
            arm_down()
            CUR_Z = 1

        elif z > 0 and CUR_Z != 2:
            print(CUR_Z)
            arm_up()
            CUR_Z = 2

    #moves robot if x and y location to move to
    if x != 4000 and y!= 4000:
        moveX = x - CUR_X
        moveY = y - CUR_Y
        #print("moveX" + "{0:2.2f} ".format(moveX) + "moveY" + "{0:2.2f} ".format(moveY))
        ep_chassis.move(x=moveX, y=moveY, z=0, xy_speed=SIMPLE_SPEED).wait_for_completed()

#///////////////execute helper function////////////////
def get_values(command):
    #The split() command is used to break apart the gcode lines.

    #removes any comments in gcode if present
    if "(" in command:
        freeCommand = command.split("(")[0]
    else:
        freeCommand = command

    if "X" in freeCommand:
        #removes letters and values before "X" including X
        afterx = freeCommand.split("X")[1]
        #removes letters and values after x value
        txtx = afterx.split()[0]
        #converts x string to flaot after printing
        x = float(txtx)/SCALE
    else:
        #to handle when their is no value. 4,000 is outside of
        #the reasonable range the robot may draw.
        x = 4000

    if "Y" in freeCommand:
        aftery = freeCommand.split("Y")[1]
        txty = aftery.split()[0]
        y = float(txty)/SCALE
    else:
        y = 4000

    if "Z" in freeCommand:
        afterz = freeCommand.split("Z")[1]
        txtz = afterz.split()[0]
        z = float(txtz)
    else:
        z = 4000

    if "F" in freeCommand:
        afterf = freeCommand.split("F")[1]
        txtf = afterf.split()[0]
        f = float(txtf)/SCALE
    else:
        f = 4000

    return x, y, z, f

#////////////////////////Sub Position Handler////////////////////////////////
def sub_position_handler(position_info):
    global CUR_X
    global CUR_Y
    global CUR_R
    CUR_X, CUR_Y, CUR_R = position_info
    #print("chassis position: x:{0}, y:{1}, z:{2}".format(x, y, z))

def arm_up():
    ep_arm.move(0, 50)
    time.sleep(1)

def arm_down():
    ep_arm.move(0,-50)
    time.sleep(1)

#///////////////CODE START/////////////////////////
#///////////////////////////////////////////////////
if __name__ == '__main__':
    #set up robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_chassis = ep_robot.chassis

    ep_arm = ep_robot.robotic_arm

    ep_gripper = ep_robot.gripper

    ep_chassis.sub_position(freq=10, callback=sub_position_handler)

    main()
# Write your code here :-)
