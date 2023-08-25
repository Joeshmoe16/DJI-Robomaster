#the goal of this section is to come up with a dance function
#when called the robot would choose a random dance

import robomaster
import time
import random
from robomaster import robot
from robomaster import led


#/////////////////////////Bee Dance///////////////////////////
def do_the_bee_dance():
    #play bee sound
    ep_robot.play_audio(filename="bees.wav")
    
    #set LED to blink yellow
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=0, effect=led.EFFECT_BREATH)
    
    #wiggle section
    speed = 0.5
    angle_speed = 360
    wiggle_time = 0.3
    ep_chassis.drive_speed(x=speed, y=0, z=-200, timeout=.2)
    time.sleep(.2)
    ep_chassis.drive_speed(x=speed, y=0, z=angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=-angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=-angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=-angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)

    #robot does a turn section
    ep_chassis.drive_speed(x=2, y=0, z=-130, timeout=1.2)
    time.sleep(1.2)

    #goes through a striagh section
    ep_chassis.drive_speed(x=2, y=0, z=0, timeout=.8)
    time.sleep(.8)

    #robot does a turn section
    ep_chassis.drive_speed(x=2, y=0, z=-130, timeout=1.2)
    time.sleep(1.3)

    #wiggle section
    ep_chassis.drive_speed(x=speed, y=0, z=-200, timeout=.2)
    time.sleep(.2)
    ep_chassis.drive_speed(x=speed, y=0, z=angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=-angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=-angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)
    ep_chassis.drive_speed(x=speed, y=0, z=-angle_speed, timeout=wiggle_time)
    time.sleep(wiggle_time)

    #robot does a turn section
    ep_chassis.drive_speed(x=2, y=0, z=130, timeout=1.5)
    time.sleep(1.5)

    #goes through a striaght section
    ep_chassis.drive_speed(x=2, y=0, z=0, timeout=.7)
    time.sleep(.7)

    #robot does a turn section
    ep_chassis.drive_speed(x=2, y=0, z=130, timeout=1.3)
    time.sleep(1.4)

    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()

    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)

    
#////////////////////////////Space Dance////////////////////////////////
def space_dance():
    #play music by Joey Shotts
    ep_robot.play_audio(filename="spacejourney8.wav")

    #set LED to blink yellow
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=255, b=0, effect=led.EFFECT_BREATH)

    space_speed = 0.2

    space_time = 1
    
    #set robot to move in diamond pattern
    for i in range(0,7):
        ep_chassis.drive_speed(x=space_speed, y=space_speed, z=0, timeout=space_time)
        time.sleep(space_time)
        ep_chassis.drive_speed(x=space_speed, y=-space_speed, z=0, timeout=space_time)
        time.sleep(space_time)
        ep_chassis.drive_speed(x=-space_speed, y=-space_speed, z=0, timeout=space_time)
        time.sleep(space_time)
        ep_chassis.drive_speed(x=-space_speed, y=space_speed, z=0, timeout=space_time)
        time.sleep(space_time)

    time.sleep(2)

    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()

    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)


#///////////////////////WALTZ///////////////////////
def waltz():
    #Open Gripper
    ep_gripper.open(power=50)
    time.sleep(1.5)
    ep_gripper.pause()
    
    #set LED to blink orange
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=150, b=0, effect=led.EFFECT_BREATH, freq = 1)

    #decide time to wait
    waltz_time = .37
    waltz_speed = .7
    
    #play music by MondayHopes (https://pixabay.com/music/search/waltz/)
    ep_robot.play_audio(filename="waltz-for-a-cat.wav")

    #gets the timing right
    time.sleep(.1)
    
    #Does Waltz Motion
    for i in range(0,7):
        #forward
        ep_chassis.drive_speed(x=waltz_speed, y=0, z=0, timeout=waltz_time)
        time.sleep(waltz_time)
        #right
        ep_chassis.drive_speed(x=0, y=waltz_speed, z=0, timeout=waltz_time)
        time.sleep(waltz_time)
        #pause
        ep_chassis.drive_speed(x=0, y=0, z=0, timeout=waltz_time)
        time.sleep(waltz_time)
        #back
        ep_chassis.drive_speed(x=-waltz_speed, y=0, z=0, timeout=waltz_time)
        time.sleep(waltz_time)
        #left
        ep_chassis.drive_speed(x=0, y=-waltz_speed, z=0, timeout=waltz_time)
        time.sleep(waltz_time)
        #pause
        ep_chassis.drive_speed(x=0, y=0, z=0, timeout=waltz_time)
        time.sleep(waltz_time)

    #wait for 2 seconds
    time.sleep(2)
    
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #Close Gripper
    ep_gripper.close(power=50)
    time.sleep(1.5)
    ep_gripper.pause()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)


#///////////////////////DISCO///////////////////////
def disco():
    #play music by MondayHopes (https://pixabay.com/music/search/waltz/), clip was shortened
    ep_robot.play_audio(filename="disco2.wav")

    #set LED to scroll
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_SCROLLING)

    #time will impact timing, speed will impact speed
    disco_time = 1
    disco_speed = 100
    
    #Does disco motion
    ep_chassis.drive_speed(x=0, y=0, z=-disco_speed, timeout=disco_time/2)
    time.sleep(disco_time/2)
    
    for i in range(0,12):
        #spin
        ep_chassis.drive_speed(x=0, y=0, z=disco_speed, timeout=disco_time)
        time.sleep(disco_time)
        ep_chassis.drive_speed(x=0, y=0, z=-disco_speed, timeout=disco_time)
        time.sleep(disco_time)

    ep_chassis.drive_speed(x=0, y=0, z=disco_speed, timeout=disco_time/2)
    time.sleep(disco_time/2)
    
    time.sleep(1)
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #Close Gripper
    ep_gripper.close(power=50)
    time.sleep(1.5)
    ep_gripper.pause()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)


#///////////////////////JAZZ///////////////////////
def jazz_hands():
    #Play Jazz Music, shortened clip
    ep_robot.play_audio(filename="jazz2.wav")

    #set LED
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_BREATH)
    
    for i in range(0,14):
        #Open Gripper
        ep_gripper.open(power=50)
        time.sleep(1.5)
        #Close Gripper
        ep_gripper.close(power=50)
        time.sleep(1.5)

    #Close Gripper
    ep_gripper.close(power=50)
    time.sleep(1.5)
    ep_gripper.pause()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)


#///////////////////////ROCK///////////////////////
def rock():
    #set LED
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)

    rock_speed = 1
    rock_time = 0.8
    
    #Play Rock Music
    ep_robot.play_audio(filename="rock2.wav")

    #gets the timing right
    time.sleep(.2)
    
    #Rocks back and forth
    for i in range(0,14):
        #spin
        ep_chassis.drive_speed(x=rock_speed, y=0, z=0, timeout=rock_time)
        time.sleep(rock_time)
        ep_chassis.drive_speed(x=-rock_speed, y=0, z=0, timeout=rock_time)
        time.sleep(rock_time)

    time.sleep(2)
    
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)

#///////////////////////BLUEGRASS///////////////////////
def bluegrass():
    #set LED
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=255, b=255, effect=led.EFFECT_BREATH)

    bluegrass_speed = 200
    bluegrass_time = 0.8
    
    #Play Rock Music
    ep_robot.play_audio(filename="bluegrass2.wav")

    #gets the timing right
    time.sleep(.2)
    
    #Rocks back and forth
    for i in range(0,30):
        #spin
        ep_chassis.drive_speed(x=0, y=0, z=bluegrass_speed, timeout=bluegrass_time)
        time.sleep(bluegrass_time)
        
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)

#///////////////////////rasputin///////////////////////
def rasputin():
    #set LED
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=0, b=0, effect=led.EFFECT_BREATH)

    #time will impact timing, speed will impact speed
    rasputin_time = .89
    rasputin_speed = 150
    
    #Play Rock Music
    ep_robot.play_audio(filename="rasputin.wav")

    #gets the timing right
    time.sleep(3.3)
    
    #Does disco motion
    ep_chassis.drive_speed(x=0, y=0, z=-rasputin_speed, timeout=rasputin_time/2)
    time.sleep(rasputin_time/2)
    
    for i in range(0,8):
        #spin
        ep_chassis.drive_speed(x=0, y=0, z=rasputin_speed, timeout=rasputin_time)
        time.sleep(rasputin_time)
        ep_chassis.drive_speed(x=0, y=0, z=-rasputin_speed, timeout=rasputin_time)
        time.sleep(rasputin_time)

    ep_chassis.drive_speed(x=0, y=0, z=rasputin_speed, timeout=rasputin_time/2)
    time.sleep(rasputin_time/2)
    
    time.sleep(2)
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)

#////////////////////////No/////////////////////
def no():
    no_time = 120
    ep_chassis.move(x=0, y=0, z=30, z_speed = no_time).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=-60, z_speed = no_time).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=60, z_speed = no_time).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=-60, z_speed = no_time).wait_for_completed()
    ep_chassis.move(x=0, y=0, z=30, z_speed = no_time).wait_for_completed()

#////////////////////////Dance//////////////////
def dance():
    choice = random.randint(0, 7)

    if choice == 0:
        space_dance()
    elif choice == 1:
        waltz()
    elif choice == 2:
        disco()
    elif choice == 3:
        jazz_hands()
    elif choice == 4:
        rock()
    elif choice == 5:
        bluegrass()
    elif choice == 6:
        rasputin()
    elif choice == 7:
        no()

#////////////MAIN CODE START//////////////////
if __name__ == '__main__':
    #Setup Connection
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    #Import Modules
    ep_chassis = ep_robot.chassis
    ep_led = ep_robot.led
    ep_gripper = ep_robot.gripper
    ep_arm = ep_robot.robotic_arm
    ep_arm.recenter().wait_for_completed()

    
    #Testing Functions
    rasputin()
    

    ep_robot.close()

    
