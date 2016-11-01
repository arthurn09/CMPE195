#!/usr/bin/env python

import cv2
import numpy as np
# import imutils


def canny(imgray):

    imgray = cv2.GaussianBlur(imgray, (5,5),200)
    thresh = cv2.Canny(imgray, 5, 200)
    # ret, th1 = cv2.threshold(thresh, 128, 255,cv2.THRESH_BINARY_INV)
    return thresh

def filter(imgray):
    minLineLength = 1
    maxLineGap = 1
    thresh = canny(imgray)
    hough = cv2.HoughLines(thresh, 1, np.pi / 180, 0)
    # hough = cv2.HoughLinesP(thresh, 2, np.pi / 180, 100, minLineLength, maxLineGap)

    print hough.shape


    # for i in range(0, hough.shape[0]):
    #     for x1, y1, x2, y2 in hough[i]:
    #         cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)


    for i in range(0,40):
        for rho, theta in hough[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            # if i == 20:
            if a != 0 or b != 1 :
                # if i == 25 and b != 1:
                x0 = a * rho
                y0 = b * rho
                x1 = int(x0 + 1000 * (-b))
                y1 = int(y0 + 1000 * (a))
                x2 = int(x0 - 1000 * (-b))
                y2 = int(y0 - 1000 * (a))
                print a
                print b

                print x0
                print y0
                print x1
                print y1
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

    return thresh

#draw detected images
#read in image
img = cv2.imread('/home/is/opencv/opencv-3.0.0-alpha/samples/python2/streetView4.jpg')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh1 = filter(imgray)
# resized_imgray = cv2.resize(thresh1, (500,500), interpolation = cv2.INTER_AREA)

resized_img = cv2.resize(img, (500,500), interpolation = cv2.INTER_AREA)

cv2.imshow('img',resized_img)

cv2.waitKey()
cv2.destroyAllWindows()

