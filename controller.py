import pygame
import socket

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputting the
# information.
class TextPrint:
    def __init__(self):
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def print(self, screen, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height
        
    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15
        
    def indent(self):
        self.x += 10
        
    def unindent(self):
        self.x -= 10
        
pygame.init()
ch0 = 0 #left tread
ch1 = 0 #right tread
ch2 = 0 #turret
ch3 = 0 #reverse switch
ch4 = 0 #cam pan
ch5 = 0 #cam tilt

# Set the width and height of the screen [width,height]
size = [500, 700]
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Pi Tank Driver")

#Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Initialize the joysticks
pygame.joystick.init()
    
# Get ready to print
textPrint = TextPrint()

#init client sender
print('enter host IP')
host = '192.168.191.37'
port = 5555
    
client_socket = socket.socket() #instantiate
client_socket.connect((host, port)) #connect to the server

# -------- Main Program Loop -----------
while done==False:
    # EVENT PROCESSING STEP
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done=True # Flag that we are done so we exit this loop
        
        # Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
        if event.type == pygame.JOYBUTTONDOWN:
            print("Joystick button pressed.")
        if event.type == pygame.JOYBUTTONUP:
            print("Joystick button released.")
            
 
    # DRAWING STEP
    # First, clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.
    screen.fill(WHITE)
    textPrint.reset()

    # Get count of joysticks
    joystick_count = pygame.joystick.get_count()

    textPrint.print(screen, "Number of joysticks: {}".format(joystick_count) )
    textPrint.indent()
    
    # For each joystick:
    for i in range(joystick_count):
        joystick = pygame.joystick.Joystick(i)
        joystick.init()
    
        textPrint.print(screen, "Joystick {}".format(i) )
        textPrint.indent()
    
        # Get the name from the OS for the controller/joystick
        name = joystick.get_name()
        textPrint.print(screen, "Joystick name: {}".format(name) )
        
        # Usually axis run in pairs, up/down for one, and left/right for
        # the other.
        axes = joystick.get_numaxes()
        textPrint.print(screen, "Number of axes: {}".format(axes) )
        textPrint.indent()
        
        for i in range( axes ):
            axis = joystick.get_axis( i )
            textPrint.print(screen, "Axis {} value: {:>6.3f}".format(i, axis) )

        textPrint.unindent()
        buttons = joystick.get_numbuttons()
        leftTread = joystick.get_axis(2)
        rightTread = joystick.get_axis(5)
        cameraPan = joystick.get_axis(0)
        #ch0 = int(abs(throttle * 100))
        #ch1 = int(abs(throttle * 100))
        ch0 = int(((leftTread +1)/2)*100)
        ch1 = int(((rightTread +1)/2)*100)
        ch2 = int(((cameraPan +1)/2)*100)
        
        #print("ch0: ",ch0, "ch1: ",ch1)
        ch2 = 50
        ch3 = 0
        for i in range( buttons ):
            button = joystick.get_button( i )
            if(i == 1 and button == 1):
                ch3 = int(100)
            # if(i == 4 and button ==1):
            #     ch2 = int(0)
            # if(i == 5 and button ==1):
            #     ch2 = int(100)

        ch0 = str(ch0)
        ch1 = str(ch1)
        ch2 = str(ch2)
        ch3 = str(ch3)
        ch4 = str(ch4)
        ch5 = str(ch5)
        
        message = str(ch0 + '/' + ch1 + '/' + ch2 + '/' + ch3 + '/' + ch4 + '/' + ch5)

        client_socket.send(message.encode()) #send message
        data = client_socket.recv(1024).decode() #receive response
 
            

        textPrint.print(screen, "Number of buttons: {}".format(buttons) )
        textPrint.indent()

        for i in range( buttons ):
            button = joystick.get_button( i )
            textPrint.print(screen, "Button {:>2} value: {}".format(i,button) )

        textPrint.unindent()
        
        # Hat switch. All or nothing for direction, not like joysticks.
        # Value comes back in an array.
        hats = joystick.get_numhats()
        textPrint.print(screen, "Number of hats: {}".format(hats) )
        textPrint.indent()

        for i in range( hats ):
            hat = joystick.get_hat( i )
            textPrint.print(screen, "Hat {} value: {}".format(i, str(hat)) )
        textPrint.unindent()
        
        textPrint.unindent()

    
    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
    
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # Limit to 20 frames per second
    clock.tick(20)
    
# Close the window and quit.
# If you forget this line, the program will 'hang'
# on exit if running from IDLE.
#close socket connection
client_socket.close()
pygame.quit ()
