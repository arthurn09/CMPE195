import socket

UDP_IP = "10.0.0.228"
UDP_PORT = 5005

f = open('data.txt' , 'r')

# Read multiple lines
#for line in f:
#   MESSAGE = line

# REad only one line
MESSAGE = f.readline()

f.close()

# MESSAGE = "Hello, World!"

print "UDP target IP:", UDP_IP

print "UDP target port:", UDP_PORT
print "message:", MESSAGE

sock = socket.socket(socket.AF_INET, # Internet

socket.SOCK_DGRAM) # UDP

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))

