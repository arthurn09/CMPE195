#!/usr/bin/env python
#written by Israel Soto

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
    
    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    video_writer = cv2.VideoWriter('tailgate2_video.avi',fourcc,5,(600,500))
    widthArray = [1 for k in range(4)]
    heightArray = [1 for h in range(4)]
    j = 0
    count = 0
    while count < 20:
        count = count + 1
        
        stream = io.BytesIO();
        with picamera.PiCamera() as camera:
            camera.resolution = (600,500);
            camera.capture(stream, format ='bmp')
        
        buff = numpy.fromstring(stream.getvalue(),dtype = numpy.uint8)
        image = cv2.imdecode(buff,1)
        results = alpr.recognize_array(bytes(bytearray(buff)))
        
        if count == 1:
            video_writer.write(image)
            cv2.imshow('Video', image)

for plate in results['results']:
    cv2.putText(frame, "Plate#: " + plate['plate'], (0,22), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,0), 2)
        cv2.putText(frame, "Tailgating!!!", (0,100), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255), 2)
            coordinatesFile = open('tailgate.log', 'a')
                coordinatesFile.write('Driver tailgating '),
                    coordinatesFile.write('%s\n' % (datetime.datetime.now()))
                        coordinatesFile.close()
                        
                        for coordinates in results['results']:
                for x in coordinates['coordinates']:
                    j+=1
                    print("x: %i y: %i" % (x['x'], x['y']))
                    widthArray.insert(j,x['x'])
                    heightArray.insert(j, x['y'])
                    if j % 4 == 0:
                        cv2.rectangle(image, (widthArray[j-3], heightArray[j-3]),(widthArray[j-3] + (widthArray[j-1] - widthArray[j]), heightArray[j-3] + (heightArray[j-1] - heightArray[j-2])), (0,255,0),2)
                        print("x: %i y: %i" % (x['x'], x['y']))
    
        video_writer.write(image)
        cv2.imshow('Video', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

##        count = count + 1

##cap.release()
cv2.destroyAllWindows()
alpr.unload()