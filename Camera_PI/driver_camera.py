import sys

sys.path.append('/usr/local/lib/python2.7/site-packages')


import cv2
import numpy
import time
import datetime

#Load a cascade file for detecting faces
face_cascade = cv2.CascadeClassifier('haarcascade_face.xml')
#Load a cascade file for detecting eyes
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

#initialize usb webcam
webcam = cv2.VideoCapture(0)

#get fps, height, and width of resolution
fps = webcam.get(5)
height = webcam.get(4)
width = webcam.get(3)

print(fps)
print(height)
print(width)

#set height and width
webcam.set(4, 300)
webcam.set(3, 200)



count = 0
while count < 20:
    ret = webcam.read()
    count += 1
count = 0
#change count to lower script
while count < 10:
    
    print(count)
    
    #capture frame
    ret, frame = webcam.read()
    
    #Convert to grayscale
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    
    #Equalize histogram
    gray = cv2.equalizeHist(gray)
    
    #Look for faces in the image using the loaded cascade file
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y), (x+w, y+h), (255, 0, 0), 2)
        roi_gray = gray[y:y+h, x:x+h]
        roi_color = frame[y:y+h, x:x+h]
    
    #does not detect any faces (driver is checking blindspot)
    if int(len(faces)) < 1:
        
        print('Driver checking blind spot')
        #blind spot check log file append
        blind_spot_check_log_file = open('blindspot.log','a')
        blind_spot_check_log_file.write('Driver checked blind spot ')
        blind_spot_check_log_file.write('%s\n' % (datetime.datetime.now()))
        blind_spot_check_log_file.close()

    #detects face (driver is not checking blindspot)
    else:
        eyes = eye_cascade.detectMultiScale(roi_gray, 1.1, 5)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        
        #does not detect two eyes (driver is distracted)
        if int(len(eyes)) < 2:
            
            print('Driver is distracted')
            #distracted log file append
            distracted = open('distracted.log', 'a')
            distracted.write('Driver distracted ')
            distracted.write('%s\n' % (datetime.datetime.now()))
            distracted.close()
        
        #detects both eyes (driver is not distrated)
        else:
            print('Driving safely')

#write image
cv2.imwrite('frame.jpg', frame)
    
    count = count + 1








