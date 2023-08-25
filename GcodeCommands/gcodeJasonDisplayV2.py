import pygame

# changes durign the game and initial value is starting pos
movePos = (0, 0)  # global
curPos = [0, 0]

def main():
    # definitions
    size = width, height = 1100, 600
    title = "Jason Gcode Moves"  # shows at top of window
    gcodeFontSize = 24
    mainLoopDelay = 300
    white = (255,255,255)

    commands = []
    texts = []

    # initialize pygame module
    pygame.init()
    # initialize font
    font = pygame.font.SysFont("sansserif", gcodeFontSize)

    # create window and title
    window = pygame.display.set_mode(size)
    pygame.display.set_caption(title)

    # create car that moves around
    jason = pygame.image.load("JasonGraphic.png")
    jasonRect = jason.get_rect()

    # Move the rectangle to startingPos
    window.fill(white)
    jasonRect = jasonRect.move(100, 300)
    window.blit(jason, jasonRect)
    pygame.display.flip()

    # open file and read line by line
    with open("star.txt", "r") as gcodeFile:
        while True:
            # reads the current line and puts it in a string.
            command = gcodeFile.readline()

            # prints out and then indexes the current line in the file. Only Prints
            # if G0 command is being run.
            if "G0" in command:
                global movePos
                # add delay and clear screen
                pygame.time.delay(mainLoopDelay)
                window.fill(white)

                # adds most recent command to a list
                commands.append(
                    command[:-1]
                )  # removes the last char in string, adds command to list

                # appends a list with the text surfaces, one for each command
                numCommands = len(commands)
                render = font.render(commands[numCommands - 1], 1, (10, 10, 10))
                texts.append(render)

                scrollCommands(texts, window)

                # Sends a line to be executed. This both reads the command
                # from the file and executes it. If no relevant command is found nothing happens.
                movePos = 0, 0
                execute(command)

                jasonRect = jasonRect.move(movePos)
                window.blit(jason, jasonRect)

                # display window
                pygame.display.flip()

            # exits the while loop when the end of the gcode is reached
            if "(end)" in command:
                break

    # wait for escape key to quit the window
    run = True
    while run:
        print(pygame.event.get())
        pygame.time.delay(100)
        keys = pygame.key.get_pressed()
        # Break the loop when ESCAPE is pressed
        if keys[pygame.K_ESCAPE]:
            run = False

    pygame.quit()


def scrollCommands(texts, window):
    gcodeFontPos = (700, 50)
    numCommands = len(texts)
    displayCommands = 5  # max number of commands that will be displayed at one time
    textHeight = 23

    # display the text input
    if numCommands > displayCommands:
        startCommand = numCommands - displayCommands
    else:
        startCommand = 0
    # Draw the text
    i = 0
    for s in texts:
        i += 1
        if i > startCommand:
            yPos = gcodeFontPos[1] - (textHeight * (-(i - startCommand)))
            window.blit(s, (gcodeFontPos[0], yPos))


# //////////////////execute: decides which command///////////////////
def execute(command):
    if "G00" in command:
        print("G00")
        x, y, z, f = get_values(command)
        G00_G01(x, y, z)

    elif "G01" in command:
        print("G01")
        x, y, z, f = get_values(command)
        G00_G01(x, y, z)

    elif "G02" in command:
        print("G02")

    elif "G03" in command:
        print("G03")
    print(command)


# /////////////////G00 and G01 Helper Function////////////////
def G00_G01(x, y, z):
    global curPos
    global movePos

    # moves robot if x and y location to move to if valid x and y values
    if x != 4000 and y != 4000:
        moveX = y - curPos[0]
        moveY = x - curPos[1]
        movePos = moveX, -moveY
        # Move the rectangle
        # print("moveX" + "{0:2.2f} ".format(movePos[0]) + "moveY" + "{0:2.2f} ".format(movePos[1]))
        curPos[0] = y
        curPos[1] = x
        #print("CUR_X" + "{0:2.2f} ".format(CUR_X) + "CUR_Y" + "{0:2.2f} ".format(CUR_Y))

# ///////////////execute helper function////////////////
def get_values(command):
    # The split() command is used to break apart the gcode lines.
    SCALE = 3
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
        x = float(txtx) * SCALE
    else:
        x = 4000

    if "Y" in freeCommand:
        aftery = freeCommand.split("Y")[1]
        txty = aftery.split()[0]
        y = float(txty) * SCALE
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
        f = float(txtf) * SCALE
    else:
        f = 4000

    return x, y, z, f


# ///////////////CODE START/////////////////////////
# ///////////////////////////////////////////////////
if __name__ == "__main__":
    main()
