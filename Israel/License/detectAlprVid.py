#!/usr/bin/env python
from openalpr import Alpr
import cv2
import numpy as np
import pprint

alpr = Alpr("us","/home/is/opencv/opencv-3.0.0-alpha/build/bin/openalpr.conf.defaults","/home/is/opencv/opencv-3.0.0-alpha/build/bin/runtime_data")
cap = cv2.VideoCapture(0)


xtotal = 0
ytotal = 0
count = 0
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

else:

    alpr.set_top_n(20)
    alpr.set_default_region("md")
    alpr.set_detect_region(False)

    widthArray = [1 for k in range(4)]
    heightArray = [1 for h in range(4)]
    j = 0
    k = 0
    n = 0
    m = 0
    count = 0
    while True:

        ret, frame = cap.read()
        ret, enc = cv2.imencode("*.bmp",frame)
        results = alpr.recognize_array(bytes(bytearray(enc)))

        for coordinates in results['results']:
            for x in coordinates['coordinates']:
                j +=1
                xtotal = xtotal + x['x']
                ytotal = ytotal + x['y']
                count = count + 1
                if count == 10:
                    print("RESULTS==========================")
                    print(xtotal/10)
                    print(ytotal/10)
                    count = 0
                    xtotal=0
                    ytotal=0


                print("x: %i y: %i" % (x['x'], x['y']))
                print("j: %i" % (j))
                widthArray.insert(j, x['x'])
                heightArray.insert(j, x['y'])
                # cv2.rectangle(frame, (widthArray[1], heightArray[1]), (widthArray[1] + (widthArray[3] - widthArray[4]), heightArray[1] + (heightArray[3] - heightArray[2])),(0, 255, 0), 2)

        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

cv2.waitKey()
cap.release()
cv2.destroyAllWindows()
alpr.unload()
