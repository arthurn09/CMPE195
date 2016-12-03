#!/usr/bin/env python

import cv2
import numpy 
import numpy as np

import sys
import time
import datetime
import io
import picamera



##cap = cv2.VideoCapture(0)

def getIntersection(line1, line2,image):

    # first line
    s1 = np.array(line1[0])
    e1 = np.array(line1[1])

    # second line
    s2 = np.array(line2[0])
    e2 = np.array(line2[1])

    a1 = (s1[1] - e1[1]) / (s1[0] - e1[0])
    b1 = s1[1] - (a1 * s1[0])

    a2 = (s2[1] - e2[1]) / (s2[0] - e2[0])
    b2 = s2[1] - (a2 * s2[0])

    if abs(a1 - a2) < sys.float_info.epsilon:
        print "Does not intersect"

    x = (b2 - b1) / (a1 - a2)
    y = a1 * x + b1

    if x > 0 and y > 0:
        print "Intersects at x: %.2f y: %.2f" % (x, y)
        intersectfile = open('laneChange.log', 'a')
        intersectfile.write('lane change \n')
        intersectfile.close()
        cv2.putText(image, "Changing lanes", (399,470),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,255),2)

    else:
        cv2.putText(image, "Driving Safe", (0,470),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0),2)

        print "You are driving safe!"



def canny(imgray):

    imgray = cv2.GaussianBlur(imgray, (5,5),200)
    thresh = cv2.Canny(imgray, 5, 200)
    # ret, th1 = cv2.threshold(thresh, 128, 255,cv2.THRESH_BINARY_INV)
    return thresh


def filter():

    fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
    video_writer = cv2.VideoWriter('lanechange_video.avi',fourcc,20,(639,479))
    count =0
    while count < 10:

##        ret, img = cap.read()
##        cv2.line(img, (322, 479), (320, 239), (255, 255, 0), 2)
        # 90.24 degrees at (321, 479), (320, 239)

        # angleofline = np.arctan2(239 - 479, 320 - 321) * 180.0 / np.pi
        # print "line: %.2f" % angleofline
    
        count = count + 1

        stream = io.BytesIO();
        with picamera.PiCamera() as camera:
            camera.resolution = (639,479);
            camera.capture(stream, format ='bmp')

        buff = numpy.fromstring(stream.getvalue(),dtype = numpy.uint8)
        image = cv2.imdecode(buff,1)
        cv2.line(image, (322, 479), (320, 239), (255, 255, 0), 2)  

        imgray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        thresh = canny(imgray)
        hough = cv2.HoughLines(thresh, 1, np.pi / 180, 0)

        for i in range(0,5):
            for rho, theta in hough[i]:

                a = np.cos(theta)
                b = np.sin(theta)

                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))

                angle = np.arctan2(y2 - y1, x2 - x1) * 180.0 / np.pi

                posAngle = abs(angle)
                intAngle = int(posAngle)



                if intAngle <= 80 and intAngle >= 10:
                    cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
                    line1 = ([322, 479], [320, 239])
                    line2 = ([x1, y1], [x2, y2])
                    getIntersection(line1, line2,image)
            
            #video_writer.write(image)
            cv2.imshow('frame', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break



#draw detected images
#read in image
# img = cv2.imread('/home/is/opencv/opencv-3.0.0-alpha/samples/python2/streetView4.jpg')

thresh1 = filter()

# resized_imgray = cv2.resize(thresh1, (500,500), interpolation = cv2.INTER_AREA)
# resized_img = cv2.resize(img, (500,500), interpolation = cv2.INTER_AREA)
# cv2.imshow('img',resized_img)

#cv2.waitKey()
cv2.destroyAllWindows()
