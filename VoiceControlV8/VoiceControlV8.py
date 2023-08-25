#This code is the latest version of the voice controlled robot.

#///////////////////////Libraries/////////////////////////////////
#for voice recognition
from vosk import Model, KaldiRecognizer

#for other purposes
import time
import cv2
import random

#for multithreading
import threading
import queue

#For robomaster control
import robomaster
from robomaster import robot
from robomaster import led


#////////////////////global Vvariable definitions//////////////////
#these are all for basic motion
X_VAL = 0.5
Y_VAL = 0.6
Z_VAL = 90
SIMPLE_SPEED = 1
SIMPLE_TURN_SPEED = 45

#for follow me function
persons = []
p_val_z = -160 #how fast jason turns
p_val_x = 1.8 #how quick he goes forward and back
height = 0.8  #how close he gets

#position definitions
HIGHEST_ARM_X = 10
HIGHEST_ARM_Y = 90


#////////////////////////////////Main/////////////////////////////////////////////
def main(): 
    #center the arm
    ep_arm.recenter().wait_for_completed()

    #initializes and starts task that turns sound into speach
    playing_task = threading.Thread(target=create_speach_task)
    playing_task.start()

    #initializes and starts task that receives sound
    playing_task = threading.Thread(target=receive_sound__task)
    playing_task.start()
    
    #sleeps while voice recognition model is opened, this is important because you
    #don't want the task to start too early
    time.sleep(6)
    
    print("#" * 80)
    print("#" * 80)
    
    print('-----Now Recording-----')
    
    #Looped Section of Code/////////////////////////////////////////////////////////////////
    #global previous_time
    previous_time = time.time()
    
    while True:
        current_time = time.time()
        millis_elapsed = (current_time - previous_time)*1000

        millis_wait = 700

        speach = q2.get()

        print(speach)
        
        #if jason is in command run the command, jason frequently gets recognized as other phrases
        names_array = {
            "jason", "chase in", "the case then", "the case i", "the chasing"
            
        }

        #loop through names array
        for name in names_array:
            #checks speach for name and makes sure enough time has passed between commands
            if name in speach and (millis_elapsed > millis_wait):
                print("running command")
                run_command(speach)
                previous_time = time.time()

        
            
def receive_sound__task():
    #starts an audio stream
    ep_camera.start_audio_stream()

    num_frames = 1
    
    while True:
        #lets you decide how many frames you want to input into the vosk recognizer,
        #seemed to work best with just one
        frames = []

        for i in range(0, num_frames):
            #the try keeps things a little safer
            try:
                frame = ep_camera.read_audio_frame()
                frames.append(bytes(frame))

                #combines the frames together so that vosk recognizer
                #can understand them
                sound_data = b''.join(frames)
                
                #puts the sound data to the queue so it can be accessed in the main loop
                q.put(sound_data)
                
            except Exception as e:
                print("LiveView: playing_task, video_frame_queue is empty.")
                continue


def create_speach_task():
    #Inititialize Vosk Model
    model = Model("vosk-model-en-us-0.22-lgraph")

    #the sample rate is determined by the microphone, robomaster has a sample rate of 48000
    the_samplerate = 48000
    vosk_recognizer = KaldiRecognizer(model, the_samplerate)

    while True:
        #gets sound from que
        sound = q.get()

        #this if/else converts the data 
        if vosk_recognizer.AcceptWaveform(sound):
            speach = vosk_recognizer.Result()
        else:
            speach = str(vosk_recognizer.PartialResult())

        #checks for stop function seperatly
        if "stop" in speach:
            stop()

        #puts speach into a second queue
        q2.put(speach)


 #///////////////////Primary Function that checks the command//////////////////
def run_command(speach):
    
    global previous_time
    
    commands_array = {
        "stop" : stop,
        "go forward": forward,
        "go for": forward,
        "go back": backward,
        "go left": left,
        "go lot": left,
        "go right": right,
        "turn left": turn_left,
        "turn lot": turn_left,
        "turn right": turn_right,
        "be dance": do_the_bee_dance,
        "dance": dance,
        "space": space_dance,
        "walls": waltz,
        "disco": disco,
        "jazz": jazz_hands,
        "rock": rock,
        "bluegrass": bluegrass,
        "donut": donuts,
        "follow": follow_me,
        "yes": yes,
        "no": no,
        "give": give,
        "take": take,
        "close": closeGrip,
        "open": openGrip,
    }


    # Use a `switch` statement to find the appropriate action for the given speech. it loops through all of the options
    for command in commands_array:
        #if it finds an option in the commands_array
        if command in speach:
            #runs command
            return commands_array[command]()


#///////////////////////stop/////////////////////////
def stop():
    #it would be smart to add additional functionality later but this is what I have for now
    print("stop")
    time.sleep(0.5)

    
#functions for basic movement///////////////////////////
def forward():
    ep_chassis.move(x=X_VAL, y=0, z=0, xy_speed=SIMPLE_SPEED).wait_for_completed()
def backward():
    ep_chassis.move(x=-X_VAL, y=0, z=0, xy_speed=SIMPLE_SPEED).wait_for_completed()
def left():
    ep_chassis.move(x=0, y=-Y_VAL, z=0, xy_speed=SIMPLE_SPEED).wait_for_completed()
def right():
    ep_chassis.move(x=0, y=Y_VAL, z=0, xy_speed=SIMPLE_SPEED).wait_for_completed()
def turn_left():
    ep_chassis.move(x=0, y=0, z=Z_VAL, z_speed=SIMPLE_TURN_SPEED).wait_for_completed()
def turn_right():
    ep_chassis.move(x=0, y=0, z=-Z_VAL, z_speed=SIMPLE_TURN_SPEED).wait_for_completed()



#//////////////////////////////////////////functions for dancing///////////////////////////////////////////
#/////////////////////////Bee Dance///////////////////////////
def dance():
    randomMove = random.randint(1,6)

    dances = {

        1:space_dance,
        2:waltz,
        3:disco,
        4:jazz_hands,
        5:rock,
        6:bluegrass,
        7:donuts,

        }

    #loops through dances
    for dance in dances:
        #checks if dance matches random number
        if randomMove == dance:
            #if the dance does match the random number it does that dance
            dances[dance]()
            
    
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
    time.sleep(.8)

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

    time.sleep(.2)
    
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
    
    #Does disco Motion
    for i in range(0,10):
        #spin
        ep_chassis.drive_speed(x=0, y=0, z=disco_speed, timeout=disco_time)
        time.sleep(disco_time)
        ep_chassis.drive_speed(x=0, y=0, z=-disco_speed, timeout=disco_time)
        time.sleep(disco_time)
        
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)


#///////////////////////JAZZ///////////////////////
def jazz_hands():
    #Play Jazz Music, shortened clip
    ep_robot.play_audio(filename="jazz2.wav")

    #set LED
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=0, b=255, effect=led.EFFECT_BREATH)
    
    for i in range(0,10):
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
    for i in range(0,15):
        ep_chassis.drive_speed(x=rock_speed, y=0, z=0, timeout=rock_time)
        time.sleep(rock_time)
        ep_chassis.drive_speed(x=-rock_speed, y=0, z=0, timeout=rock_time)
        time.sleep(rock_time)
        
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)

#///////////////////////BLUEGRASS///////////////////////
def bluegrass():
    #set LED
    ep_led.set_led(comp=led.COMP_ALL, r=0, g=255, b=255, effect=led.EFFECT_BREATH)

    bluegrass_speed = 200
    bluegrass_time = 27
    
    #Play Rock Music
    ep_robot.play_audio(filename="bluegrass2.wav")

    #gets the timing right
    time.sleep(1)
    
    
    #spin
    ep_chassis.drive_speed(x=0, y=0, z=bluegrass_speed, timeout=bluegrass_time)
    time.sleep(bluegrass_time)
        
    #stops robot
    ep_chassis.move(x=0.1, y=0, z=0).wait_for_completed()
    
    #resets LEDS
    ep_led.set_led(comp=led.COMP_ALL, r=255, g=255, b=255, effect=led.EFFECT_ON)


def donuts():
    donuts_time = 12
    ep_chassis.drive_speed(x=0, y=0.5, z=-40, timeout=donuts_time)

    for i in range(0, 5):
        #Play Rock Music
        ep_robot.play_audio(filename="wheelscreah.wav").wait_for_completed()
    

    
#//////////////////////////////////////////FOLLOW FUNCTIONS///////////////////////
#//////////////////follow_me()/////////////////////
class PersonInfo:

    def __init__(self, x, y, w, h):
        self._x = x
        self._y = y
        self._w = w
        self._h = h

    @property
    def pt1(self):
        return int((self._x - self._w / 2) * 1280), int((self._y - self._h / 2) * 720)

    @property
    def pt2(self):
        return int((self._x + self._w / 2) * 1280), int((self._y + self._h / 2) * 720)

    @property
    def center(self):
        return int(self._x * 1280), int(self._y * 720)

def on_detect_person(person_info):
    number = len(person_info)
    persons.clear()
    for i in range(0, number):
        x, y, w, h = person_info[i]
        persons.append(PersonInfo(x, y, w, h))

    #if collecting data on one person move the robot
    if number == 1:
        x, y, w, h = person_info[0]
        print("person: x:{0}, y:{1}, w:{2}, h:{3}".format(x, y, w, h))
        
        error_z = 0.5 - x
        move_z = error_z*p_val_z
        
        error_x = (0.5 - y) - (h - height)
        move_x = error_x*p_val_x

        #print("Z:{0}, X:{1}".format(move_z, move_x))
        ep_chassis.drive_speed(x=move_x, y=0, z=move_z, timeout = .5)
 
def follow_me():
    #move arm to better veiwing angle
    global HIGHEST_ARM_Y
    global HIGHEST_ARM_X
    
    #highest
    ep_arm.move(HIGHEST_ARM_X, HIGHEST_ARM_Y).wait_for_completed()
    
    ep_camera.start_video_stream(False)
    result = ep_vision.sub_detect_info(name="person", callback=on_detect_person)

    for i in range(0, 1000):
        img = ep_camera.read_cv2_image(strategy="newest", timeout=0.5)
        for j in range(0, len(persons)):
            cv2.rectangle(img, persons[j].pt1, persons[j].pt2, (255, 255, 255))
        cv2.imshow("Persons", img)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    result = ep_vision.unsub_detect_info(name="person")
    cv2.destroyAllWindows()
    ep_camera.stop_video_stream()

    #move back to default arm position
    ep_arm.recenter().wait_for_completed()
    

#////////////////ROBOTIC ARM CONTROL////////////////////////
def openGrip():
    ep_gripper.open(power=50)
    time.sleep(1.5)
    ep_gripper.pause()

def closeGrip():
    ep_gripper.close(power=50)
    time.sleep(1.5)
    ep_gripper.pause()

def take():
    global HIGHEST_ARM_Y
    global HIGHEST_ARM_X
    
    #highest
    ep_arm.move(HIGHEST_ARM_X, HIGHEST_ARM_Y)
    
    openGrip()
    time.sleep(2)
    closeGrip()
    
    #move back to default arm position
    ep_arm.recenter().wait_for_completed()

def give():
    global HIGHEST_ARM_Y
    global HIGHEST_ARM_X
    #highest
    ep_arm.move(HIGHEST_ARM_X, HIGHEST_ARM_Y)

    time.sleep(2)
    openGrip()
    closeGrip()
    time.sleep(1)
    
    #move back to default arm position
    ep_arm.recenter().wait_for_completed()


#///////////////////////////YES AND NO//////////////////////
def yes():
    global HIGHEST_ARM_Y
    global HIGHEST_ARM_X
    
    #highest
    ep_arm.move(HIGHEST_ARM_X, HIGHEST_ARM_Y).wait_for_completed()

    #move back to default arm position
    ep_arm.recenter().wait_for_completed()

    #highest
    ep_arm.move(HIGHEST_ARM_X, HIGHEST_ARM_Y).wait_for_completed()

    #move back to default arm position
    ep_arm.recenter().wait_for_completed()


def no():
    ep_chassis.move(x=0, y=0.4, z=0).wait_for_completed()
    ep_chassis.move(x=0, y=-0.8, z=0).wait_for_completed()
    ep_chassis.move(x=0, y=0.8, z=0).wait_for_completed()
    ep_chassis.move(x=0, y=-0.4, z=0).wait_for_completed()


  
#///////////////CODE START/////////////////////////
#///////////////////////////////////////////////////
if __name__ == '__main__':
    #set up robot
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")
    
    ep_chassis = ep_robot.chassis
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_led = ep_robot.led
    ep_gripper = ep_robot.gripper
    ep_arm = ep_robot.robotic_arm
    
    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    
    #opens queue that command will be written to
    #q is for sound data
    q = queue.Queue()
    
    #q2 is for speach data
    q2 = queue.Queue()
    
    main()
