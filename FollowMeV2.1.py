# -*-coding:utf-8-*-
# Copyright (c) 2020 DJI.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License in the file LICENSE.txt or at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import cv2
import robomaster
from robomaster import robot
from robomaster import vision


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


persons = []

p_val_z = -180
p_val_x = 2.0

#Must be a value from 0-1. the smaller the number
#the smaller they will appear in the frame
height = 0.8

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
        
        error_x = (0.5 - y) - (h - .9)
        move_x = error_x*p_val_x

        #print("Z:{0}, X:{1}".format(move_z, move_x))
        ep_chassis.drive_speed(x=move_x, y=0, z=move_z, timeout = .5)
        
if __name__ == '__main__':
    ep_robot = robot.Robot()
    ep_robot.initialize(conn_type="ap")

    ep_vision = ep_robot.vision
    ep_camera = ep_robot.camera
    ep_chassis = ep_robot.chassis
    ep_arm = ep_robot.robotic_arm
    
    #move arm to better veiwing angle
    #position definitions
    HIGHEST_ARM_X = 10
    HIGHEST_ARM_Y = 90
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
    
    ep_robot.close()
