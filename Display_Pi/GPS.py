# Reference
# http://www.danmandle.com/blog/getting-gpsd-to-work-with-python/
 
import os
from gps import *
from time import *
import time
import threading
import fcntl

gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while gpsp.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
  gpsp = GpsPoller() # create the thread
  try:
    gpsp.start() # start it up
    while True:
      speed = int(gps.fix.speed * 2.23694)
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
 
      os.system('clear')
      f = open("speed.txt",'w')
      fcntl.flock(f, fcntl.LOCK_EX)
      f.write('%i'%(speed))
      fcntl.flock(f, fcntl.LOCK_UN)
      f.close()
      print
      print 'MPH         ' , speed
 
      time.sleep(5) #set to whatever
 
