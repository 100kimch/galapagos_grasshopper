# NOTE: detecting crosswalk using roadview

import cv2
import numpy as np
import pathlib

path = pathlib.Path().absolute()
print(path)
size = 3
kernel = np.ones((size, size), np.float32) / (size * size)

img_general = cv2.imread(str(path) + '/assets/images/sample_bicycle_13.png')
img_roadview = cv2.imread(str(path) + '/assets/images/sample_bicycle_16.png')
img_roadview_hsv = cv2.cvtColor(img_roadview, cv2.COLOR_BGR2HSV)
colors_roadview = [(80, 0, 0), (110, 255, 255)]
mask_roadview = cv2.inRange(
    img_roadview_hsv, colors_roadview[0], colors_roadview[1])
mask_roadview = cv2.medianBlur(mask_roadview, 5)
# mask_roadview = cv2.dilate(mask_roadview, kernel)

template = cv2.imread(str(path) + '/assets/images/sample_pattern_04.png', 0)
w, h = template.shape[::-1]

# WGY
colors_low = [(20, 6, 227), (21, 131, 223), (25, 40, 220)]
colors_high = [(25, 12, 233), (22, 134, 226), (28, 50, 240)]
# colors_low = [(25, 38, 226), (22, 6, 225)]
# colors_high = [(30, 50, 235), (25, 13, 235)]

cv2.namedWindow('testing')
cv2.namedWindow('testing2')
cv2.moveWindow('testing', 1790, 0)
cv2.moveWindow('testing2', 2300, 0)
while True:
    # ret, frame = cap.read()
    frame = img_general

    filtered = cv2.filter2D(frame, -1, kernel)

    if frame is None:
        break

    frame_cross = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for low, high in zip(colors_low, colors_high):
        frame_cross = cv2.bitwise_or(
            frame_cross, cv2.inRange(frame_hsv, low, high), cv2.COLOR_BGR2GRAY)
    frame_cross = cv2.medianBlur(frame_cross, 3)

    frame_template = cv2.matchTemplate(
        frame_cross, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(frame_template >= 0.8)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(frame_template, pt,
                      (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    # frame_cross = cv2.dilate(frame_cross, kernel)
    corners = cv2.cornerHarris(frame_cross & mask_roadview, 25, 15, 0.14)
    frame_corners = cv2.cvtColor(
        frame_cross & mask_roadview, cv2.COLOR_GRAY2BGR)
    frame_corners[corners > 0.01 * corners.max()] = [0, 0, 255]

    cv2.imshow('testing', frame_cross)
    cv2.imshow('testing2', frame_corners)

    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv2.imwrite(str(path) + '/assets/images/sample_bicycle_14.png', frame_cross)
cv2.imwrite(str(path) + '/assets/images/sample_bicycle_15.png', frame_corners)
