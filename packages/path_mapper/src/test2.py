# NOTE: detecting all roads where have traffic jam data
import cv2
import numpy as np
import pathlib

path = pathlib.Path().absolute()
print(path)
cap = cv2.imread(str(path) + '/assets/images/sample_bicycle_04.png')

# ROYB
colors_low = [(2, 20, 225), (17, 25, 240), (25, 65, 230), (51, 70, 210)]
colors_high = [(4, 204, 255), (21, 180, 255), (27, 180, 255), (55, 170, 255)]

size = 11
kernel = np.ones((size, size), np.float32) / (size * size)

cv2.namedWindow('testing')
cv2.namedWindow('testing2')
cv2.moveWindow('testing', 1790, 0)
cv2.moveWindow('testing2', 2300, 0)
while True:
    # ret, frame = cap.read()
    frame = cap

    filtered = cv2.filter2D(frame, -1, kernel)

    if frame is None:
        break

    frame_arrows = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for low, high in zip(colors_low, colors_high):
        frame_arrows = cv2.bitwise_or(
            frame_arrows, cv2.inRange(frame_hsv, low, high), cv2.COLOR_BGR2GRAY)

    frame_arrows = cv2.dilate(frame_arrows, kernel)
    corners = cv2.cornerHarris(frame_arrows, 15, 3, 0.14)
    frame_corners = cv2.cvtColor(frame_arrows, cv2.COLOR_GRAY2BGR)
    frame_corners[corners > 0.01 * corners.max()] = [0, 0, 255]

    cv2.imshow('testing', frame)
    cv2.imshow('testing2', frame_corners)

    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break

# cv2.imwrite(str(path) + '/assets/images/sample_bicycle_06.png', frame_corners)
# cv2.imwrite(str(path) + '/assets/images/sample_bicycle_06.png', frame_arrows)
