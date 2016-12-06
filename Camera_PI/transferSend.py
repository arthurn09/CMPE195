#written by Eduardo Lemus
##Reference
#https://www.youtube.com/watch?v=u6kuHMY5pHM

import socket

UDP_IP = "169.254.23.217"

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








