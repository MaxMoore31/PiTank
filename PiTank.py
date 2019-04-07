import RPi.GPIO as GPIO
import time
from pynput import keyboard
from pynput.keyboard import Listener
import socket
import csv

#init server code
host = ''
port = 5555 #init port
server_socket = socket.socket() #get instance
server_socket.bind((host, port)) #bind host adress and port together

#config how many clients at one time
server_socket.listen(2)
conn, address = server_socket.accept() #accept new conn
print("connection from: " + str(address))

#init variables
msPerCycle = 1000/50
fullStick = 2.5 #100 percent power
deadStick = 0.5 #zero percent power
GPIO.setmode(GPIO.BOARD) #init GPIO packaged to reference board pins.
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT) #init pin 7 as output pin
treadLeft = GPIO.PWM(7, 50) #begin PWM signal at 50Hz
GPIO.setup(40, GPIO.OUT) #init PWM signal at 50Hz
treadRight = GPIO.PWM(40, 50) #begin PWM signal at 50Hz
GPIO.setup(11, GPIO.OUT) #init PWM signal at 50Hz
turretTravers = GPIO.PWM(11, 50) #begin PWM signal at 50Hz
GPIO.setup(13, GPIO.OUT) #init PWM signal at 50Hz
reverse = GPIO.PWM(13, 50) #begin PWM signal at 50Hz

#begin tank at idle
dutyCyclePercentage = deadStick * 100/msPerCycle #calculate duty cycle percentage for zero pwoer
l.start(dutyCyclePercentage) #left tread, zero power
dutyCyclePercentage = deadStick * 100/msPerCycle #calculate duty cycle percentage for zero power
r.start(dutyCyclePercentage) #right tread, zero power

def leftTreadOn(): #activated the left tread, in future will take argument for percentage throttle
    dutyCyclePercentage = fullStick * 100/msPerCycle
    treadLeft.start(dutyCyclePercentage)
def rightTreadOn(): #activated the right tread, in future will take argument for percentage throttle
    dutyCyclePercentage = fullStick * 100/msPerCycle
    treadRight.start(dutyCyclePercentage)
    
def leftTreadOff(): #deactivated the left tread, in future will take argument for percentage throttle
    dutyCyclePercentage = deadStick * 100/msPerCycle
    treadLeft.start(dutyCyclePercentage)
def rightTreadOff(): #deactivated the right tread, in future will take argument for percentage throttle
    dutyCyclePercentage = deadStick * 100/msPerCycle
    treadRight.start(dutyCyclePercentage)
    
def leftTreadControl(input): #pass control values the left tread, in future will take argument for percentage throttle
    control = 0.5
    input = (input*2)/100
    control = control + input
    dutyCyclePercentage = control * 100/msPerCycle
    treadLeft.start(dutyCyclePercentage)
    print('left tread: ' + input)
    
def rightTreadControl(input): #pass control values the right tread, in future will take argument for percentage throttle
    control = 0.5
    input = (input*2)/100
    control = control + input
    dutyCyclePercentage = control * 100/msPerCycle
    treadRight.start(dutyCyclePercentage)
    print('right tread: ' + input)
    
    def reverse(input): #activated the right tread, in future will take argument for percentage throttle
        if(input < 50):
            dutyCyclePercentage = fullStick * 100/msPerCycle
            reverse.start(dutyCyclePercentage)
    


while True:
    #recieve data stream
    data = conn.recv(1024).decode()
    

    chanArray = data.split("/")
    print(chanArray)
    leftTreadChan = float(chanArray[0])
    rightTreadChan = float(chanArray[1])
    turretRot = float(chanArray[2])
    reverse =  float(chanArray[3])
    
    leftTreadControl(leftTreadChan)
    rightTreadControl(rightTreadChan)
    reverse(reverse)

    if not data:
        break
    data = 'ACK'
    conn.send(data.encode())
    
conn.close()

# def on_press(key): #onpress key handler
    
    # if key == keyboard.Key.left: #!reassign to WASD
        # #print("a")
        # leftTreadOn()
    # if key == keyboard.Key.right:
        # print("d")
        # rightTreadOn()
        
# def on_release(key): #onrelease key handler
    # #print("{0} I ".format(str(key)))
    # if key == keyboard.Key.left:
        # print("left")
        # leftTreadOff()
    # if key == keyboard.Key.right:
        # print("right")
        # rightTreadOff()



#leftPos = 0.75
#rightPos = 2.5
#middlePos = (rightPos - leftPos)/2+leftPos
#posList = [leftPos, middlePos, rightPos, middlePos]


try:
    with Listener( #activate listener
        on_press=on_press,
        on_release=on_release) as listener:
        listener.join()
    print("standby")
    while True:
        time.sleep(0.1)
        

    
except KeyboardInterrupt: #break out of infinite loop
    p.stop()
    GPIO.cleanup()
    print("done")
    
    
        #for position in posList:
          #  dutyCyclePercentage = position * 100/msPerCycle
            #p.start(dutyCyclePercentage)
            #time.sleep(0.5)
        
