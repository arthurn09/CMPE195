import socket
import fcntl

#add flag for read from file and add multiple lines

#UDP_IP = "10.0.0.228" 
#UPD_IP = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
UPD_IP = 169.254.23.217
UDP_PORT = 5005

f = open('send_data.txt' , 'r')
fcntl.flock(f, fcntl.LOCK_EX)

# Read multiple lines
#for line in f:
#   MESSAGE = line

# REad only one line
MESSAGE = f.read()

fcntl.flock(f, fcntl.LOCK_UN)
f.close()

# MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP

print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet

socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

