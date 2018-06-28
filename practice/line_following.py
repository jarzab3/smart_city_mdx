import time
import cv2
import numpy as np

camera = cv2.VideoCapture(0)

time.sleep(0.1)

while True:
    (grabbed, image) = camera.read()

    # image = frame.array

    roi = image[200:250, 0:639]

    Blackline = cv2.inRange(roi, (0,0,0), (110, 110, 110))

    kernel = np.ones((3, 3), np.uint8)

    Blackline = cv2.erode(Blackline, kernel, iterations=5)
    Blackline = cv2.dilate(Blackline, kernel, iterations=9)

    # cv2.imshow("Black line", Blackline)

    img,contours, hierarchy = cv2.findContours(Blackline.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) > 0:
        x,y,w,h = cv2.boundingRect(contours[0])

        # cv2.line(image, (x + int(w/2), 200), (x+ int(w/2), 250),(200,80,80), 10)

        cv2.circle(image, ((x + int(w/2)), (y + int(h/2))), 8, (200, 80, 80), -1)


    cv2.imshow("orginal with line", image)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
