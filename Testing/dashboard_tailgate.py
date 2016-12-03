#!/usr/bin/env python
from openalpr import Alpr
import cv2
import io
import picamera
import numpy
import pprint
from time import sleep
import datetime

#cap = cv2.VideoCapture(0)

alpr = Alpr("us","/home/pi/opencv-3.0.0/build/bin/openalpr.conf.defaults","/home/pi/opencv-3.0.0/build/bin/runtime_data")

if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

else:
    
    alpr.set_top_n(20)
    alpr.set_default_region("md")
    alpr.set_detect_region(False)
    
    count = 0
    while count < 10
        #ret, frame = cap.read()
        #ret, enc = cv2.imencode("*.bmp",frame)
        #results = alpr.recognize_array(bytes(bytearray(enc)))    

        stream = io.BytesIO();
        with picamera.PiCamera() as camera:
            camera.resolution = (300,200);
            camera.capture(stream, format ='bmp')

        buff = numpy.fromstring(stream.getvalue(),dtype = numpy.uint8)
        image = cv2.imdecode(buff,1)
        results = alpr.recognize_array(bytes(bytearray(buff)))        
    
        for coordinates in results['results']:
            for x in coordinates['coordinates']:
                print("x: %i y: %i" % (x['x'], x['y']))
                coordinatesFile = open('tailgate.log', 'a')
                coordinatesFile.write('Driver tailgating '),
                coordinatesFile.write('%s\n' % (datetime.datetime.now()))
                coordinatesFile.close()
        cv2.imshow('Video', image)


        count = count + 1

cap.release()
cv2.destroyAllWindows()
alpr.unload()
