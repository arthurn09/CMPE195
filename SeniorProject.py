import io
import picamera
import cv2
import numpy
import time


#start general timer
start = time.time()

#total time when texting
textAmt = 0

#total time for speeding
speedAmt = 0

#total time for tailgating
tailgatingAmt = 0

#swerving indicator code here...

#dangerous lane change indicator here ...

#total time for running entire program
totalTime = 0

#Forever while loop
var =1
while var == 1:
    
    #timer for beginning of interval
    initialTime = time.time()
    
    #Create a memory stream so photos doesn't need to be saved in a file
    stream = io.BytesIO()

    #Get the picture (low resolution, so it should be quite fast)
    #Here you can also specify other parameters (e.g.:rotate the image)
    with picamera.PiCamera() as camera:
        camera.resolution = (300,200)
        #2592 , 1944 max resolution, lower resolution = better difference between texting and paying attention
        camera.capture(stream, format='jpeg')

    #Convert the picture into a numpy array
    buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)

    #Now creates an OpenCV image
    image = cv2.imdecode(buff, 1)

    #Load a cascade file for detecting faces
    face_cascade = cv2.CascadeClassifier('/home/pi/Desktop/haarcascade_eye.xml')
    #'/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml'
    #cd /data/haarcascades/haarcascade_froarcascade_eye.xml

    #Convert to grayscale
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    #Look for eyes in the image using the loaded cascade file
    eyes = face_cascade.detectMultiScale(gray, 1.1, 5)

    print "Found "+str(len(eyes))+" eyes"

    #not paying attention to road
    if int(len(eyes)) < 2:
        print "Keep eyes on the road!"
        #gets current time
        textTime = time.time()
        #increments text time
        textAmt = textAmt + (textTime-initialTime)

    #Draw a rectangle around every found face
    for (x,y,w,h) in eyes:
        cv2.rectangle(image,(x,y),(x+w,y+h),(255,255,0),2)

    #Save the result image
    cv2.imwrite('result.jpg',image)

    #speeding detection code here ...

    #tailgating detection code here ...

    #swerving detection code here ...

    #dangerous lane change code here ...

    #timer for end of interval
    end = time.time()

    #increment total time
    totalTime = totalTime + (end - start)

    #percentage of time spent texting during drive
    textPercent = sleepAmt/totalTime
    print "Text percentage: " + str(textPercent) + "%"
    


