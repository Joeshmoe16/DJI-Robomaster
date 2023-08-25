import time
import math
import matplotlib.pyplot as plt
import numpy as np

# ////////////////////global Variable definitions//////////////////
# these are all for basic motion
CUR_X = 0
CUR_Y = 0
CUR_Z = 3

SCALE = 0.005


def main():
    commands = []
    with open("earthPic_0001.txt", "r") as gcodeFile:
        # repeats until end of file is reached (or error is thrown)
        while True:
            # reads the current line and puts it in a string.
            line = gcodeFile.readline()

            if "G0" in line:
                commands.append(line)

            # exits the while loop when the end of the gcode is reached
            if "(end)" in line:
                break  # Write your code here :-)
    print("processing commands")
    for command in commands:
        execute(command)

    ax.set(
        xlim=(-1, 5),
        xticks=np.arange(0, 5),
        ylim=(-1, 5),
        yticks=np.arange(0, 5),
    )

    print("loading plot")
    plt.show()


# //////////////////execute: decides which command///////////////////
def execute(command):
    if "G00" in command:
        x, y, z, f, I, J = get_values(command)
        G00_G01(x, y, z)
    elif "G01" in command:
        x, y, z, f, I, J = get_values(command)
        G00_G01(x, y, z)
    elif "G02" in command:
        x, y, z, f, I, J = get_values(command)
        G02(x, y, I, J)
    elif "G03" in command:
        x, y, z, f, I, J = get_values(command)
        G03(x, y, I, J)


# ///////////////execute helper function////////////////
def get_values(command):
    print(command)
    # The split() command is used to break apart the gcode lines.
    # removes any comments in gcode if present
    if "(" in command:
        freeCommand = command.split("(")[0]
    else:
        freeCommand = command
    if "X" in freeCommand:
        # removes letters and values before "X" including X
        afterx = freeCommand.split("X")[1]
        # removes letters and values after x value
        txtx = afterx.split()[0]
        # converts x string to flaot after printing
        x = (float(txtx)) * SCALE
    else:
        # to handle when their is no value. 4,000 is outside of
        # the reasonable range the robot may draw.
        x = 4000
    if "Y" in freeCommand:
        aftery = freeCommand.split("Y")[1]
        txty = aftery.split()[0]
        y = (float(txty)) * SCALE
    else:
        y = 4000
    if "Z" in freeCommand:
        afterz = freeCommand.split("Z")[1]
        txtz = afterz.split()[0]
        z = float(txtz) * SCALE
    else:
        z = 4000
    if "F" in freeCommand:
        afterf = freeCommand.split("F")[1]
        txtf = afterf.split()[0]
        f = float(txtf)
    else:
        f = 4000
    if "I" in freeCommand:
        aftery = freeCommand.split("I")[1]
        txty = aftery.split()[0]
        I = float(txty) * SCALE
    else:
        I = 4000
    if "J" in freeCommand:
        aftery = freeCommand.split("J")[1]
        txty = aftery.split()[0]
        J = float(txty) * SCALE
    else:
        J = 4000
    return x, y, z, f, I, J


# /////////////////G00 and G01 Helper Function////////////////
def G00_G01(x, y, z):
    # moves chalk down if neg. z or up if pos. z
    global CUR_Z
    global CUR_X
    global CUR_Y

    if z != 4000:
        if z < 0 and CUR_Z != 1:
            # print(CUR_Z)
            # arm_down()
            CUR_Z = 1
        elif z > 0 and CUR_Z != 2:
            # print(CUR_Z)
            # arm_up()
            CUR_Z = 2

    # moves robot if x and y location to move to
    if x != 4000 and y != 4000:
        # moveX = (x*SCALE - CUR_X)
        # moveY = (y*SCALE - CUR_Y)
        # print("moveX" + "{0:2.2f} ".format(moveX) + "moveY" + "{0:2.2f} ".format(moveY))
        # ep_chassis.move(x=moveX, y=moveY, z=0, xy_speed=SIMPLE_SPEED).wait_for_completed()
        CUR_X = x
        CUR_Y = y

        ax.scatter(CUR_X, CUR_Y, s=20, c=80, vmin=0, vmax=100)


# //////////////////////////G02 function/////////////////////////////
def G02(X, Y, I, J):
    global CUR_X
    global CUR_Y
    # create arc object
    arcOne = G02_G03(True, CUR_X, CUR_Y, X, Y, I, J)
    # get the start angle of the arc
    start = int(arcOne.arcStartAngle())
    print(start)
    #get the end angle of the arc
    end = int(arcOne.arcEndAngle())
    print(end)

    if (end > start) and (end != 360):
        # print("end smaller")
        G02_Helper(arcOne, start, 0)
        G02_Helper(arcOne, 360, end)
    else:
        # print("end greater")
        G02_Helper(arcOne, start, end)
    # stop()
    CUR_X = X
    CUR_Y = Y


def G02_Helper(arcOne, start, end):
    prevTarX = 0
    prevTarY = 0
    # get the aproximate time of the arc
    delay = arcOne.arcTime(1, 1)
    startTime = time.time()
    for i in range(start, end, -1):
        # gets the current angle
        val = i
        # calculates the tar position for the robot at that angle
        tarY = arcOne.tarY(val)
        tarX = arcOne.tarX(val)

        # print("(" + "{0:2.2f} ".format(tarX) + ", " + "{0:2.2f} ".format(tarY))

        ax.scatter(tarX, tarY, s=20, c=80, vmin=0, vmax=100)

        # time.sleep(delay)
        prevTarX = tarX
        prevTarY = tarY

        # this is just here as a safety feature, it times out if the robot has been moving for too long
        if (time.time() - startTime) > 10:
            print("missed major target")
            break


# //////////////////////////G03 function/////////////////////////////
def G03(X, Y, I, J):
    global CUR_X
    global CUR_Y
    # create arc object
    arcOne = G02_G03(True, CUR_X, CUR_Y, X, Y, I, J)
    # get the start angle of the arc
    start = int(arcOne.arcStartAngle())
    # print(start)
    # get the end angle of the arc
    end = int(arcOne.arcEndAngle())
    # print(end)

    if (end < start) and (end != 360):
        # print("end smaller")
        G03_Helper(arcOne, start, 360)
        G03_Helper(arcOne, 0, end)
    else:
        # print("end greater")
        G03_Helper(arcOne, start, end)
    # stop()
    CUR_X = X
    CUR_Y = Y


def G03_Helper(arcOne, start, end):
    prevTarX = 0
    prevTarY = 0
    # get the aproximate time of the arc
    delay = arcOne.arcTime(1, 1)
    startTime = time.time()

    for i in range(start, end):
        # gets the current angle
        val = i

        # calculates the tar position for the robot at that angle
        tarY = arcOne.tarY(val)
        tarX = arcOne.tarX(val)

        # print("(" + "{0:2.2f} ".format(tarX) + ", " + "{0:2.2f} ".format(tarY))

        ax.scatter(tarX, tarY, s=20, c=80, vmin=0, vmax=100)

        # time.sleep(delay)
        prevTarX = tarX
        prevTarY = tarY

        # this is just here as a safety feature, it times out if the robot has been moving for too long
        if (time.time() - startTime) > 10:
            print("missed major target")
            break


# this class helps to get different values asociated with the G02 and G03 arcs
class G02_G03:
    def __init__(self, isG02, curX, curY, X, Y, I, J):
        self.isG02 = isG02  # G02 is True, G03 is False
        self.curX = curX
        self.curY = curY
        self.X = X
        self.Y = Y
        self.H = I + curX
        self.K = J + curY
        term = abs(((X - self.H) ** 2) + ((Y - self.K) ** 2))
        r = math.sqrt(term)
        self.R = r

    def tarY(self, angle):
        rad = math.radians(angle)
        tarX = (math.sin(rad) * self.R) + self.K
        return tarX

    def tarX(self, angle):
        rad = math.radians(angle)
        tarX = (math.cos(rad) * self.R) + self.H
        return tarX

    def arcStartAngle(self):
        # first determine what 'qaudrant' of the circle you are in with an imaginary
        # origin in the middle
        boolOne = self.curX >= self.H
        boolTwo = self.curY >= self.K

        # quad one
        if boolOne and boolTwo:
            term = (self.curY - self.K) / self.R
            if term >= 1:
                term = 1
            elif term <= -1:
                term = -1
            angleRad = math.asin(term)
            angle = math.degrees(angleRad)
        # quad two
        elif (not boolOne) and boolTwo:
            term = (self.curY - self.K) / self.R
            if term >= 1:
                term = 1
            elif term <= -1:
                term = -1
            angleRad = math.asin(term)
            angle = 180 - math.degrees(angleRad)
        # quad 3
        elif (not boolOne) and (not boolTwo):
            term = (self.K - self.curY) / self.R
            if term >= 1:
                term = 1
            elif term <= -1:
                term = -1
            angleRad = math.asin(term)
            angle = 180 + math.degrees(angleRad)
        # quad 4
        elif boolOne and (not boolTwo):
            term = (self.K - self.curY) / self.R
            if term >= 1:
                term = 1
            elif term <= -1:
                term = -1
            angleRad = math.asin(term)
            angle = 360 - math.degrees(angleRad)
        return angle

    def arcEndAngle(self):
        # first determine what 'qaudrant' of the circle you are in with an imaginary
        # origin in the middle
        boolOne = self.X >= self.H
        boolTwo = self.Y >= self.K

        # quad one
        if boolOne and boolTwo:
            angleRad = math.asin((self.Y - self.K) / self.R)
            angle = math.degrees(angleRad)
        # quad two
        elif (not boolOne) and boolTwo:
            angleRad = math.asin((self.Y - self.K) / self.R)
            angle = 180 - math.degrees(angleRad)
        # quad 3
        elif (not boolOne) and (not boolTwo):
            angleRad = math.asin((self.K - self.Y) / self.R)
            angle = 180 + math.degrees(angleRad)
        # quad 4
        elif boolOne and (not boolTwo):
            angleRad = math.asin((self.K - self.Y) / self.R)
            angle = 360 - math.degrees(angleRad)
        return angle

    def arcTime(self, arcDegLength, speed):
        circ = abs(2 * math.pi * self.R)
        length = (arcDegLength / 360) * circ
        time = length / speed
        return time


# ///////////////CODE START/////////////////////////
# ///////////////////////////////////////////////////
if __name__ == "__main__":
    plt.style.use("_mpl-gallery")

    # plot
    fig, ax = plt.subplots()
    main()
