# NOTE: detecting crosswalk algorithm

import cv2
import numpy as np
import pathlib
import urllib.request


def get_map_image(point, level=2, type="2d"):
    x, y, w, h = point
    map_ret = []
    for j in range(h, 0, -1):
        map_x = []
        for i in range(w):
            url = 'https://map0.daumcdn.net/{}/2009alo/L{}/{}/{}.png'.format(
                'map_' + type + '_hd', level, y + j, x + i)
            print('url: ', url)
            resp = urllib.request.urlopen(url)
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            map_x.append(cv2.imdecode(image, cv2.IMREAD_COLOR))
        map_ret.append(np.concatenate(tuple(map_x), axis=1))
    return np.concatenate(tuple(map_ret), axis=0)


def url_to_image(url):
    resp = urllib.request.urlopen(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image


def url_to_image2(url1, url2):
    resp = urllib.request.urlopen(url1)
    image1 = np.asarray(bytearray(resp.read()), dtype="uint8")
    image1 = cv2.imdecode(image1, cv2.IMREAD_COLOR)

    resp = urllib.request.urlopen(url2)
    image2 = np.asarray(bytearray(resp.read()), dtype="uint8")
    image2 = cv2.imdecode(image2, cv2.IMREAD_COLOR)

    ret = np.concatenate((image1, image2), axis=0)
    # image = cv2.imdecode(ret, cv2.IMREAD_COLOR)
    return ret


path = pathlib.Path(__file__).parents[3].absolute()
print(path)
size = 3
kernel = np.ones((size, size), np.float32) / (size * size)


kernel_dilate = np.ones((15, 15), np.float32) / (15 * 15)

# img_general = cv2.imread(
#     str(path) + '/assets/images/sample_bicycle_19.png')
# img_road = cv2.imread(
#     str(path) + '/assets/images/sample_bicycle_21.png')

# img_general = url_to_image(
#     'https://map0.daumcdn.net/map_2d_hd/2009alo/L3/1972/820.png')
# img_road = url_to_image(
#     'https://map0.daumcdn.net/map_usedistrict_hd/2009alo/L3/1972/820.png')

targets = {
    'sinjungdong': (1642, 3940, 4, 4),
    'simgok': (1643, 3944, 3, 3),
    'chuni': (1649, 3941, 3, 3)
}
img_general = get_map_image(targets['sinjungdong'], type="2d")
img_road = get_map_image(targets['sinjungdong'], type="usedistrict")

# img_test = url_to_image2(
#     'https://map0.daumcdn.net/map_2d_hd/2009alo/L3/1972/820.png',
#     'https://map0.daumcdn.net/map_usedistrict_hd/2009alo/L3/1972/820.png')
print('shape: ', img_general.shape)
# exit
img_road_hsv = cv2.cvtColor(img_road, cv2.COLOR_BGR2HSV)

# NOTE: 1st - white, 2nd - subway lines or dark colors, 3rd - wide orange roads, 4th - wide yellow roads, 5th - small yellow roads, 6th - small red roads
colors_road_low = [(0, 0, 250), (0, 88, 0),
                   (22, 138, 250), (27, 72, 230), (27, 25, 230), (176, 0, 225)]
colors_road_high = [(180, 5, 255), (180, 255, 150),
                    (28, 142, 255), (30, 74, 255), (30, 48, 255), (180, 48, 255)]

mask_road = np.zeros(
    (img_general.shape[0], img_general.shape[1]), np.uint8)
for l, h in zip(colors_road_low, colors_road_high):
    mask_road = mask_road | cv2.inRange(img_road_hsv, l, h)
# TODO: solve number label noise
mask_road = cv2.medianBlur(mask_road, 13)
# mask_road = cv2.dilate(mask_road, kernel)

template = cv2.imread(
    str(path) + '/assets/images/sample_pattern_04.png', 0)
w, h = template.shape[::-1]

# NOTE: 123 - WGYO
colors_low = [(15, 3, 227), (21, 131, 223), (25, 40, 220), (20, 140, 226)]
colors_high = [(25, 12, 233), (22, 134, 226), (28, 50, 240), (23, 160, 234)]
# colors_low = [(25, 38, 226), (22, 6, 225)]
# colors_high = [(30, 50, 235), (25, 13, 235)]

cv2.namedWindow('testing')
cv2.namedWindow('testing2')
cv2.namedWindow('testing3')
cv2.namedWindow('testing4')
cv2.moveWindow('testing', 1790, 0)
cv2.moveWindow('testing2', 2300, 0)
cv2.moveWindow('testing3', 0, 0)
cv2.moveWindow('testing4', 900, 0)
while True:
    # ret, frame = cap.read()
    frame = img_general

    # filtered = cv2.filter2D(frame, -1, kernel)

    if frame is None:
        break

    frame_cross = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
    frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    for low, high in zip(colors_low, colors_high):
        frame_cross = cv2.bitwise_or(
            frame_cross, cv2.inRange(frame_hsv, low, high), cv2.COLOR_BGR2GRAY)
    frame_cross = cv2.medianBlur(frame_cross, 3)
    frame_cross = frame_cross & mask_road

    frame_hough = cv2.erode(frame_cross, np.ones((3, 3), np.float32))
    frame_hough = cv2.dilate(frame_hough, np.ones((20, 20), np.float32))
    # frame_hough = cv2.Canny(frame_hough, 50, 50, apertureSize=3)
    # frame_hough = cv2.dilate(frame_hough, kernel)

    contours, _ = cv2.findContours(
        frame_hough, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    minRect = [None] * len(contours)
    for i, c in enumerate(contours):
        minRect[i] = cv2.minAreaRect(c)

    frame_hough = cv2.cvtColor(frame_hough, cv2.COLOR_GRAY2BGR)

    for i, c in enumerate(contours):
        color = (255, 100, 100)
        cv2.drawContours(frame_hough, contours, i, color, 3)
        box = cv2.boxPoints(minRect[i])
        # np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
        box = np.intp(box)
        cv2.drawContours(frame_hough, [box], 0, (0, 0, 255), 3)

    # ret, thr = cv2.threshold(frame_hough, 127, 255, 0)
    # contours, _ = cv2.findContours(
    #     thr, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # contours_poly = [None] * len(contours)
    # boundRect = [None] * len(contours)
    # centers = [None] * len(contours)
    # radius = [None] * len(contours)
    # for i, c in enumerate(contours):
    #     contours_poly[i] = cv2.approxPolyDP(c, 10, True)
    #     boundRect[i] = cv2.boundingRect(contours_poly[i])
    #     # centers[i], radius[i] = cv2.minEnclosingCircle(contours_poly[i])

    # frame_hough = cv2.cvtColor(frame_hough, cv2.COLOR_GRAY2BGR)

    # for i in range(len(contours)):
    #     color = (255, 100, 100)
    #     cv2.drawContours(frame_hough, contours_poly, i, color)
    #     cv2.rectangle(frame_hough, (int(boundRect[i][0]), int(boundRect[i][1])), (int(
    #         boundRect[i][0] + boundRect[i][2]), int(boundRect[i][1] + boundRect[i][3])), color, 2)
    #     # cv2.circle(frame_hough, (int(centers[i][0]), int(centers[i][1])), int(radius[i]), color, 2)

    # cnt = contours[5]
    # x, y, w, h = cv2.boundingRect(cnt)
    # cv2.rectangle(frame_hough, (x, y), (x + w, y + h), (0, 0, 255), 3)

    # rect = cv2.minAreaRect(cnt)
    # box = cv2.boxPoints(rect)
    # box = np.int0(box)

    # frame_hough = cv2.cvtColor(frame_hough, cv2.COLOR_GRAY2BGR)

    # cv2.drawContours(frame_hough, [box], 0, (0, 255, 0), 3)

    # contours, hierarchy = cv2.findContours(
    #     frame_hough, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # frame_hough = cv2.cvtColor(frame_hough, cv2.COLOR_GRAY2BGR)

    # for i in contours:
    #     hull = cv2.convexHull(i, clockwise=True)
    #     cv2.drawContours(frame_hough, [hull], 0, (0, 0, 255), 2)

    # lines = cv2.HoughLinesP(frame_hough, 1, np.pi / 180,
    #                         100, minLineLength=3, maxLineGap=20)
    # # lines = cv2.HoughLinesP(frame_hough, )
    # frame_hough = cv2.cvtColor(frame_hough, cv2.COLOR_GRAY2BGR)
    # if len(lines):
    #     for line in lines:
    #         x1, y1, x2, y2 = line[0]
    #         cv2.line(frame_hough, (x1, y1), (x2, y2), (30, 240, 30), 5)

    # frame_template = cv2.matchTemplate(
    #     frame_cross, template, cv2.TM_CCOEFF_NORMED)
    # loc = np.where(frame_template >= 0.8)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(frame_template, pt,
    #                   (pt[0] + w, pt[1] + h), (0, 255, 255), 2)

    # # frame_cross = cv2.dilate(frame_cross, kernel)
    # corners = cv2.cornerHarris(frame_cross & mask_road, 25, 15, 0.14)
    # frame_corners = cv2.cvtColor(
    #     frame_cross & mask_road, cv2.COLOR_GRAY2BGR)
    # frame_corners[corners > 0.01 * corners.max()] = [0, 0, 255]

    cv2.imshow('testing', frame_cross)
    cv2.imshow('testing2', mask_road)
    cv2.imshow('testing3', frame)
    # cv2.imshow('testing4', img_road)
    cv2.imshow('testing4', frame_hough)

    key = cv2.waitKey(30)
    if key == ord('q') or key == 27:
        break

cv2.imwrite(str(path) + '/assets/images/sample_bicycle_25.png', img_general)
cv2.imwrite(str(path) + '/assets/images/sample_bicycle_26.png', img_road)
cv2.imwrite(str(path) + '/assets/images/sample_bicycle_27.png', mask_road)
cv2.imwrite(str(path) + '/assets/images/sample_bicycle_28.png', frame_cross)
cv2.imwrite(str(path) + '/assets/images/sample_bicycle_29.png', frame_hough)
