import numpy as np
import cv2

# img = cv2.imread('capture_63.jpg', 1)
img = cv2.imread('cap.png', 1)

# capture = cv2.VideoCapture(0)

gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
cv2.imshow("Binary", thresh)

_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

img2 = img.copy()
index = -1
thickness = 4
color = (255, 0, 255)

objects = np.zeros([img.shape[0], img.shape[1],3], 'uint8')


def check_for_shapes(cnt):
    approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
    # print(len(approx))
    # if len(approx) == 5:
    #     print("pentagon")
    #     cv2.drawContours(img, [cnt], 0, 255, -1)
    # elif len(approx) == 3:
    #     print("triangle")
    #     cv2.drawContours(img, [cnt], 0, (0, 255, 0), -1)
    if len(approx) == 4:
        print("square")
        cv2.drawContours(img, [cnt], 0, (0, 0, 255), -1)
        return True
    # elif len(approx) == 9:
    #     print("half-circle")
    #     cv2.drawContours(img, [cnt], 0, (255, 255, 0), -1)
    # elif len(approx) > 15:
    #     print("circle")
    #     cv2.drawContours(img, [cnt], 0, (0, 255, 255), -1)
    #     return True

    return None

for c in contours:
    perimeter = cv2.arcLength(c, True)

    if perimeter > 10:
        shape_name = check_for_shapes(c)
        cv2.drawContours(objects, [c], -1, color, -1)
        area = cv2.contourArea(c)

        print("Perimeter ", perimeter)
        M = cv2.moments(c)

        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0

        # cx = int(M['m10']/M['m00'])
        # cy = int(M['m01']/M['m00'])
        if shape_name:
            cv2.circle(objects, (cx, cy), 4, (0, 0, 255), -1)

        # cv2.putText(objects, , (230, 50), font, 0.8, (0, 255, 0), 2, cv.LINE_AA)

        # print("Area: {}, perimeter: {}".format(area,perimeter))

cv2.imshow("Contours", objects)

cv2.waitKey(0)
cv2.destroyAllWindows()
