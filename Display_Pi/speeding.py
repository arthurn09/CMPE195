#!/usr/bin/python
import fcntl
import time

data = "Speeding " + '%s\n' % (time.strftime("%Y-%m-%d %H:%M:%S"))

f = open("data.txt","a") #opens file with name of "trial.txt"

fcntl.flock(f, fcntl.LOCK_EX)

print "Message:", data # prints to console

f.write(data) # writes to file

fcntl.flock(f, fcntl.LOCK_UN)

f.close()