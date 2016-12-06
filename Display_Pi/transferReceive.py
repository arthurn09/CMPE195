#written by Eduardo Lemus
##Reference
#https://www.youtube.com/watch?v=u6kuHMY5pHM
import socket
import fcntl

UDP_IP = "169.254.23.217"

UDP_PORT = 5005

print UDP_IP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
sock.bind((UDP_IP, UDP_PORT))


while True:

	data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes

	f = open("receive_data.txt","a") #opens file with name of "trial.txt"

    fcntl.flock(f, fcntl.LOCK_EX)
    
	print "received message:", data # prints to console

	f.write(data) # writes to file

    fcntl.flock(f, fcntl.LOCK_UN)
    
	f.close()
