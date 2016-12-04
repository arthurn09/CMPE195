import socket

#add flag for read from file and add multiple lines

UDP_IP = "169.254.23.217" 
#UPD_IP = [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]

UDP_PORT = 5005

sock = socket.socket(socket.AF_INET, # Internet
                     
socket.SOCK_DGRAM) # UDP

print "UDP target IP:", UDP_IP

print "UDP target port:", UDP_PORT

with open('send_data.txt') as fp:
    for MESSAGE in fp:
        print "message:", MESSAGE
        sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))


#reset file
f = open('send_data.txt' , 'w')
f.close()

#f = open('send_data.txt' , 'r')

# Read multiple lines
#for line in f:
#   MESSAGE = line

# REad only one line


#f.close()

# MESSAGE = "Hello, World!"







