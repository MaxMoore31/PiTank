import socket

def server_program():
	#get host name
	host = ''
	port = 5555 #init port
	x = 0
	server_socket = socket.socket() #get instance
	server_socket.bind((host, port)) #bind host adress and port together
	
	#config how many clients at one time
	server_socket.listen(2)
	conn, address = server_socket.accept() #accept new conn
	print("connection from: " + str(address))
	while True:
		#recieve data stream
		data = conn.recv(1024).decode()
		if not data:
			break
			
		print("from connected user: " + str(data))
	
		str(y) = x
		data = y
		conn.send(data.encode())
		x = x+1
	conn.close()
	
if __name__ == '__main__':
	server_program()
	