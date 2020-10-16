# NOTE: detecting bicycle roads only
import cv2
import numpy
import pathlib

path = pathlib.Path().absolute()
print(path)
cap = cv2.imread(str(path) + '/assets/images/sample_bicycle_01.png')

size = 11
kernel = numpy.ones((size, size), numpy.float32) / (size * size)

cv2.namedWindow('testing')
cv2.moveWindow('testing', 1800, 0)
while True:
    # ret, frame = cap.read()
    frame = cap

    filtered = cv2.filter2D(frame, -1, kernel)

    if frame is None:
        break

    # frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_threshold = cv2.inRange(frame, (198, 115, 100), (218, 135, 120))
    frame_threshold = cv2.medianBlur(frame_threshold, 3)
    # corners = cv2.goodFeaturesToTrack(frame_threshold, 200, 0.5, 10)
    corners = cv2.cornerHarris(frame_threshold, 15, 3, 0.14)
    frame_corners = cv2.cvtColor(frame_threshold, cv2.COLOR_GRAY2BGR)
    frame_corners[corners > 0.01 * corners.max()] = [0, 0, 255]
    # for corner in corners:
    #     x, y = corner.ravel()
    #     cv2.circle(frame_corners, (x, y), 3, 255, -1)

    cv2.imshow('testing', frame_corners)

    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv2.imwrite(str(path) + '/assets/images/sample_bicycle_2.png', frame_corners)
