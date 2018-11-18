import RPi.GPIO as GPIO
import time
from pynput import keyboard
from pynput.keyboard import Listener
from inputs import devices

#init variables
msPerCycle = 1000/50
fullStick = 2.5
deadStick = 0.5
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)
l = GPIO.PWM(7, 50)
GPIO.setup(40, GPIO.OUT)
r = GPIO.PWM(40, 50)

#begin tank at idle
dutyCyclePercentage = deadStick * 100/msPerCycle
l.start(dutyCyclePercentage)
dutyCyclePercentage = deadStick * 100/msPerCycle
r.start(dutyCyclePercentage)

def leftTreadOn():
    dutyCyclePercentage = fullStick * 100/msPerCycle
    l.start(dutyCyclePercentage)
def rightTreadOn():
    dutyCyclePercentage = fullStick * 100/msPerCycle
    r.start(dutyCyclePercentage)
    
def leftTreadOff():
    dutyCyclePercentage = deadStick * 100/msPerCycle
    l.start(dutyCyclePercentage)
def rightTreadOff():
    dutyCyclePercentage = deadStick * 100/msPerCycle
    r.start(dutyCyclePercentage)


def on_press(key):
    if key == keyboard.Key.left:
        print("left")
        leftTreadOn()
    if key == keyboard.Key.right:
        print("right")
        rightTreadOn()
        
def on_release(key):
    #print("{0} I ".format(str(key)))
    if key == keyboard.Key.left:
        print("left")
        leftTreadOff()
    if key == keyboard.Key.right:
        print("right")
        rightTreadOff()



#leftPos = 0.75
#rightPos = 2.5
#middlePos = (rightPos - leftPos)/2+leftPos
#posList = [leftPos, middlePos, rightPos, middlePos]


try:
    with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()
    print("standby")
    while True:
        time.sleep(0.1)
        

    
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    print("done")
    
    
        #for position in posList:
          #  dutyCyclePercentage = position * 100/msPerCycle
            #p.start(dutyCyclePercentage)
            #time.sleep(0.5)
        
