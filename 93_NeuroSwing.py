#!/usr/bin/env python3

from ev3dev.ev3 import *
from math import *
from time import *
from random import random
import threading

speedB = 0
speedC = 0
pos = 0

moving_average = 0
moving_average_old = 0

state_gyro = 0

class brain():
    def __init__(self):
        self.Black = 1
        self.White = 1

BrainLeft = brain()
BrainRight = brain()

btn = Button()

B = LargeMotor('outB')
C = LargeMotor('outC')

gyro = GyroSensor("in4")
gyro.mode = "GYRO-RATE"
gyro.mode = "GYRO-ANG"
gyro.mode = "GYRO-RATE"

sleep(1)
B.run_forever(speed_sp=80)
C.run_forever(speed_sp=80)
sleep(3)

B.stop(stop_action="brake")
C.stop(stop_action="brake")
sleep(1)

B.reset()
C.reset()

B.run_to_rel_pos(position_sp=-120, speed_sp=80)
C.run_to_rel_pos(position_sp=-120, speed_sp=80)
while any(C.state): sleep(0.1)

B.stop(stop_action="brake")
C.stop(stop_action="brake")

sleep(1)
B.reset()
C.reset()

Sound.speak('Ready').wait()

stop = False

def reg():

    while not stop:

        speedB = ((-1*pos)-B.position)*8
        speedC = (pos-C.position)*8

        if(speedB > 900): speedB = 900
        if(speedB < -900): speedB = -900
        if(speedC > 900): speedC = 900
        if(speedC < -900): speedC = -900

        B.run_forever(speed_sp=speedB)
        C.run_forever(speed_sp=speedC)

        sleep(0.01)

t = threading.Thread(target=reg)
t.daemon = True
t.start()

max_speed = 0

while not stop:

    stop = btn.backspace
    
    state_gyro_speed = gyro.value()
        
    if(state_gyro_speed != 0): 
        state_gyro = state_gyro_speed/abs(state_gyro_speed)
        if(state_gyro > 0):
            if(random() <= (BrainLeft.Black/(BrainLeft.Black + BrainLeft.White))): pos = -100
            else: pos = 100
        else:
            if(random() <= (BrainRight.Black/(BrainRight.Black + BrainRight.White))): pos = -100
            else: pos = 100
            
    moving_average_old = moving_average
 
    sleep(0.25)

    moving_average = abs(state_gyro_speed)*0.1 + moving_average*0.9

    if(state_gyro > 0):
        if(moving_average >= moving_average_old): 
            if(pos<0): BrainLeft.Black += 1
            else: BrainLeft.White += 1
        else:
            if(pos<0 and BrainLeft.Black > 1): BrainLeft.Black -= 1
            elif(pos>0 and BrainLeft.White > 1): BrainLeft.White -= 1

    elif(state_gyro < 0):
        if(moving_average >= moving_average_old): 
            if(pos<0): BrainRight.Black += 1
            else: BrainRight.White += 1
        else:
            if(pos<0 and BrainRight.Black > 1): BrainRight.Black -= 1
            elif(pos>0 and BrainRight.White > 1): BrainRight.White -= 1

    print("[[ " + str(BrainLeft.Black) + ", " + str(BrainLeft.White) + "][ " + str(BrainRight.Black) + ", " + str(BrainRight.White) + "]]",moving_average)


    if moving_average > max_speed + 25:
        print("[[ " + str(BrainLeft.Black) + ", " + str(BrainLeft.White) + "][ " + str(BrainRight.Black) + ", " + str(BrainRight.White) + "]]",moving_average)
        max_speed = moving_average
        if max_speed < 200:
            Sound.speak('New Record')
        else:
            Sound.speak('Learning Complete')

Sound.beep().wait() 
B.stop(stop_action="brake")
C.stop(stop_action="brake")


Sound.speak('Stop').wait()

print("[[ " + str(BrainLeft.Black) + ", " + str(BrainLeft.White) + "][ " + str(BrainRight.Black) + ", " + str(BrainRight.White) + "]]")
