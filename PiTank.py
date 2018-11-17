import RPi.GPIO as GPIO
import time
from pynput import keyboard

def on_press(key):
    if key == keyboard.key.left:
        print("left")
    if key == keyboard.key.right:
        print("right")
        



GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)
p = GPIO.PWM(7, 50)
p.start(50)
leftPos = 0.75
rightPos = 2.5
middlePos = (rightPos - leftPos)/2+leftPos
posList = [leftPos, middlePos, rightPos, middlePos]
msPerCycle = 1000/50
try:
    print("standby")
    time.sleep(5)
        

    
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
    print("done")
    
    
        #for position in posList:
          #  dutyCyclePercentage = position * 100/msPerCycle
            #p.start(dutyCyclePercentage)
            #time.sleep(0.5)
        