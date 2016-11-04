#!/usr/bin/env python

import cv2
import numpy as np
# import imutils

cap = cv2.VideoCapture(0)

def canny(imgray):

    imgray = cv2.GaussianBlur(imgray, (5,5),200)
    thresh = cv2.Canny(imgray, 5, 200)
    # ret, th1 = cv2.threshold(thresh, 128, 255,cv2.THRESH_BINARY_INV)
    return thresh

def filter():


    while True:
        ret, img = cap.read()
        imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = canny(imgray)
        hough = cv2.HoughLines(thresh, 1, np.pi / 180, 0)
        for i in range(0,40):
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

                print "angle:%i" % intAngle
                if intAngle <= 80 and intAngle >= 10:
                    cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    print "step: %i" % i

        cv2.imshow('frame', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    return thresh

#draw detected images
#read in image
# img = cv2.imread('/home/is/opencv/opencv-3.0.0-alpha/samples/python2/streetView4.jpg')


thresh1 = filter()

# resized_imgray = cv2.resize(thresh1, (500,500), interpolation = cv2.INTER_AREA)
# resized_img = cv2.resize(img, (500,500), interpolation = cv2.INTER_AREA)
# cv2.imshow('img',resized_img)

cv2.waitKey()
cv2.destroyAllWindows()

