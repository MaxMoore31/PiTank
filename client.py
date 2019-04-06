import socket

def client_program():
	host = socket.gethostname()
	port = 5555
	
	client_socket = socket.socket() #instantiate
	client_socket.connect((host, port)) #connect to the server
	
	message = input(" -> ") # take input
	
	while message.lower().strip() != 'bye':
		client_socket.send(message.encode()) #send message
		data = client_socket.recv(1024).decode() #receive response
		
		print("received from server: " + data) #print to terminal
		
		message = input(" -> ")
		
	client_socket.close()
	
if __name__ == '__main__':
	client_program()