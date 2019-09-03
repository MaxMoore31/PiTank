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
GPIO.setmode(GPIO.BCM) #init GPIO packaged to reference GPIO pins
in1 = 24
in2 = 23
in3 = 27
in4 = 22
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3,GPIO.OUT)
GPIO.setup(in4,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)

leftTreadForward = GPIO.PWM(in1,1)
leftTreadBackward = GPIO.PWM(in2,1)
rightTreadForward = GPIO.PWM(in3,1)
rightTreadBackward = GPIO.PWM(in4,1)



    
def leftTreadOff(): #deactivated the left tread, in future will take argument for percentage throttle
    leftTreadForward.stop()
def rightTreadOff(): #deactivated the right tread, in future will take argument for percentage throttle
    rightTreadForward.stop()
    
def leftTreadControl(input, reverse): #pass control values the left tread, in future will take argument for percentage throttle
    
    # if reverse < 50:
        leftTreadForward.start(True)
        leftTreadBackward.stop()
        leftTreadForward.ChangeDutyCycle(input)
        print("Left Forward")
    # if reverse > 50:
    #     leftTreadBackward.start(True)
    #     GPIO.output(in1,GPIO.LOW)
    #     leftTreadBackward.ChangeDutyCycle(input)
    #     print("Left Reverse")
    
    
    
    
def rightTreadControl(input, reverse): #pass control values the right tread, in future will take argument for percentage throttle
#    if reverse < 50:
        rightTreadForward.start(True)
        rightTreadBackward.stop()
        rightTreadForward.ChangeDutyCycle(input)
        print("Right Forward")
#    if reverse > 50:
#        rightTreadBackward.start(True)
#        GPIO.output(in3,GPIO.LOW)
#        rightTreadBackward.ChangeDutyCycle(input)
#        print("Right Backward")
   

while True:
    #recieve data stream
    data = conn.recv(1024).decode()
    

    chanArray = data.split("/")
    print(chanArray)
    leftTreadChan = float(chanArray[0])
    rightTreadChan = float(chanArray[1])
    turretRot = float(chanArray[2])
    reverse =  int(chanArray[3])
    print("reverse:" , reverse)
    
    time.sleep(10)
    
    leftTreadControl(leftTreadChan, reverse)
    
    rightTreadControl(rightTreadChan, reverse)
        
    #reverseGear(reverse)

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
        
