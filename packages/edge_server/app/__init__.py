# NOTE: detecting crosswalk algorithm
from flask import Flask, render_template, send_file, jsonify
import cv2
import numpy as np
import pathlib
import urllib.request


def do_image_processing():
    def get_map_image(point, level=2, type="2d"):
        x, y, w, h = point
        map_ret = []
        print('loading map images..')
        for j in range(h, 0, -1):
            map_x = []
            for i in range(w):
                url = 'https://map0.daumcdn.net/{}/2009alo/L{}/{}/{}.png'.format(
                    'map_' + type + '_hd', level, y + j, x + i)
                print('\r\turl: ', url)
                resp = urllib.request.urlopen(url)
                image = np.asarray(bytearray(resp.read()), dtype="uint8")
                map_x.append(cv2.imdecode(image, cv2.IMREAD_COLOR))
            map_ret.append(np.concatenate(tuple(map_x), axis=1))
        return np.concatenate(tuple(map_ret), axis=0)

    def get_kernel(size=3):
        return np.ones((size, size), np.float32) / (size * size)

    path = pathlib.Path(__file__).parents[1].absolute()
    # path = pathlib.Path(__file__).absolute()
    print(path)
    # size = 3
    # kernel = np.ones((size, size), np.float32) / (size * size)
    # kernel_dilate = np.ones((15, 15), np.float32) / (15 * 15)

    targets = {
        'sinjungdong': (1642, 3940, 4, 4),
        'simgok': (1643, 3944, 3, 3),
        'chuni': (1649, 3941, 3, 3),
        'bucheon': (1644, 3924, 5, 5),
        'konkuk': (1844, 3974, 4, 4)
    }
    img_general = get_map_image(targets['sinjungdong'], type="2d")
    img_road = get_map_image(targets['sinjungdong'], type="usedistrict")
    print('shape: ', img_general.shape)

    img_road_hsv = cv2.cvtColor(img_road, cv2.COLOR_BGR2HSV)

    # NOTE: specification
    #   1st - white
    #   2nd - subway lines or any dark colors # needs to be checked!
    #   3rd - wide orange roads
    #   4th - wide yellow roads
    #   5th - small yellow roads
    #   6th - small red roads
    #   7th - green subway line
    colors_road_low = [(0, 0, 250), (0, 88, 0),
                       (22, 138, 250), (27, 72, 230), (27, 25, 230), (176, 0, 225), (60, 230, 169)]
    colors_road_high = [(180, 5, 255), (180, 255, 125),
                        (28, 142, 255), (30, 74, 255), (30, 48, 255), (180, 48, 255), (62, 235, 172)]

    # NOTE: 1st - area_text
    colors_road_erase_low = [(21, 250, 118), (63, 0, 82)]
    colors_road_erase_high = [(23, 255, 121), (65, 5, 85)]

    mask_road = np.zeros(
        (img_general.shape[0], img_general.shape[1]), np.uint8)
    mask_road_erase = np.zeros(
        (img_general.shape[0], img_general.shape[1]), np.uint8)

    for l, h in zip(colors_road_low, colors_road_high):
        mask_road = mask_road | cv2.inRange(img_road_hsv, l, h)
    for l, h in zip(colors_road_erase_low, colors_road_erase_high):
        mask_road_erase = mask_road_erase | cv2.inRange(img_road_hsv, l, h)

    # TODO: solve number label noise
    mask_road_erase = cv2.bitwise_not(
        cv2.dilate(mask_road_erase, get_kernel(13)))
    mask_road = cv2.medianBlur(mask_road, 11) & mask_road_erase
    # mask_road = cv2.dilate(mask_road, kernel)

    template = cv2.imread(
        str(path) + '/assets/images/sample_pattern_04.png', 0)
    w, h = template.shape[::-1]

    # NOTE: 123 - WGYO
    colors_low = [(15, 3, 227), (21, 131, 223), (25, 40, 220), (20, 140, 226)]
    colors_high = [(25, 12, 233), (22, 134, 226),
                   (28, 50, 240), (23, 160, 234)]

    # cv2.namedWindow('testing2')
    # cv2.namedWindow('testing')
    # cv2.namedWindow('testing3')
    # cv2.namedWindow('testing4')
    # cv2.moveWindow('testing2', -1080, 0)
    # cv2.moveWindow('testing', -700, 0)
    # cv2.moveWindow('testing3', 0, 0)
    # cv2.moveWindow('testing4', 1000, 0)
    # while True:
    for i in [1]:
        frame = img_general

        if frame is None:
            break

        frame_cross = np.zeros((frame.shape[0], frame.shape[1], 1), np.uint8)
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        for low, high in zip(colors_low, colors_high):
            frame_cross = cv2.bitwise_or(
                frame_cross, cv2.inRange(frame_hsv, low, high), cv2.COLOR_BGR2GRAY)
        frame_cross = cv2.medianBlur(frame_cross, 3)
        frame_cross = frame_cross & mask_road

        frame_hough = cv2.erode(frame_cross, get_kernel(3))
        frame_hough = cv2.dilate(frame_hough, get_kernel(20))
        # frame_hough = cv2.Canny(frame_hough, 50, 50, apertureSize=3)
        # frame_hough = cv2.dilate(frame_hough, kernel)

        contours, _ = cv2.findContours(
            frame_hough, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        minRect = [None] * len(contours)
        for i, c in enumerate(contours):
            minRect[i] = cv2.minAreaRect(c)

        frame_hough = cv2.cvtColor(frame_hough, cv2.COLOR_GRAY2BGR)

        font = cv2.FONT_HERSHEY_SIMPLEX
        crosswalks = []
        grouped_crosswalks = []
        for i, c in enumerate(contours):
            crosswalks.append({
                'id': i,
                'ctr': (int(minRect[i][0][0]), int(minRect[i][0][1])),
                'size': (int(minRect[i][1][0]), int(minRect[i][1][1])),
                'deg': float('{:.2f}'.format(minRect[i][2])) % 180,
                # np.intp: Integer used for indexing (same as C ssize_t; normally either int32 or int64)
                'boxPoints': np.intp(cv2.boxPoints(minRect[i])),
                'merged': False
            })

        print('{} crosswalks found.'.format(len(crosswalks)))
        for i in range(len(crosswalks)):
            for j in range(i + 1, len(crosswalks)):
                c_i, c_j = crosswalks[i], crosswalks[j]
                d_x, d_y = abs(c_i['ctr'][0] - c_j['ctr'][0]), abs(
                    c_i['ctr'][1] - c_j['ctr'][1])
                print('i: {:2d} j: {:2d} d: {:4d}\t'.format(
                    i, j, d_x + d_y), end='')

                deg = abs(c_i['deg'] - c_j['deg'])
                # print('size: ', c_i['size'][0] * c_i['size'][1])
                # NOTE: when crosswalk's size is too small, assume that it has no traffic signals.
                # if (c_i['size'][0] * c_i['size'][1] < 3000):
                #     c_i['id'] = -1
                #     break
                # NOTE: when two crosswalks seem to be in an intersection, do this:
                # if (d_x + d_y < 150 and (min(deg, 90 - deg) < 17)):
                #     # _id = c_i['id']
                #     c_j['id'] = -1

                #     _ctr = [-1, -1]
                #     for a in [0, 1]:
                #         if c_i['ctr'][a] < c_j['ctr'][a]:
                #             _ctr[a] = c_i['ctr'][a] + \
                #                 (d_x * c_j['ctr'][a] //
                #                  (c_i['ctr'][a] + c_j['ctr'][a]))
                #         else:
                #             _ctr[a] = c_j['ctr'][a] + \
                #                 (d_y * c_i['ctr'][a] //
                #                  (c_i['ctr'][a] + c_j['ctr'][a]))

                #     c_i['ctr'] = (_ctr[0], _ctr[1])
                #     c_i['size'] = ((c_i['size'][0] + c_j['size'][0]) + d_x,
                #                    (c_i['size'][1] + c_j['size'][1]) + d_y)
                #     # c_i['deg'] = (c_i['deg'] + c_j['deg']) // 2
                #     c_i['boxPoints'] = np.intp(cv2.boxPoints((
                #         c_i['ctr'], c_i['size'], c_i['deg'])))
                #     c_i['merged'] = True
            print()

        print('done.')

        frame_result = cv2.cvtColor(np.copy(frame_cross), cv2.COLOR_GRAY2BGR)
        for c in crosswalks:
            if (c['id'] == -1):
                continue

            roi = cv2.cvtColor(cv2.getRectSubPix(
                frame_result, tuple(c['size']), tuple(c['ctr'])), cv2.COLOR_BGR2GRAY)

            # if (c['merged']):
            #     contours, _ = cv2.findContours(
            #         roi, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE, )

            #     print('merge shape: ', len(contours))

            #     minRect = [None] * len(contours)
            #     for ii, cc in enumerate(contours):
            #         minRect[ii] = cv2.minAreaRect(cc)

            #         c['ctr'] = (int(minRect[ii][0][0]), int(minRect[ii][0][1]))
            #         c['size'] = (int(minRect[ii][1][0]), int(minRect[ii][1][1]))
            #         c['deg'] = float('{: .2f}'.format(minRect[ii][2])) % 180
            #         c['boxPoints'] = np.intp(cv2.boxPoints(minRect[ii]))

            #     roi = cv2.cvtColor(cv2.getRectSubPix(
            #         frame_result, tuple(c['size']), tuple(c['ctr'])), cv2.COLOR_BGR2GRAY)

            # if (c['id'] == 22):
            #     saved_roi = np.copy(roi)
            hist = cv2.calcHist([cv2.erode(roi, get_kernel(3))], [0],
                                None, [2], [0, 256]).tolist()
            hist = (int(hist[0][0]), int(hist[1][0]))
            # print('hist: ', hist)
            density = hist[1] / (hist[0] + 1)
            print("#{} deg:{:3.2f} den:{:3.2f}".format(
                c['id'], c['deg'], density))
            cv2.putText(
                frame_result, '    #{} den: {:.2f}'.format(c['id'], density), c['ctr'], font, 1, (50, 50, 230), 2, cv2.LINE_AA)

            color = (255, 100, 100) if c['merged'] else (100, 100, 255)
            if (density > 0.25):
                color = (100, 255, 100)

            # cv2.drawContours(frame_result, contours, i, color, 3)
            # box = cv2.boxPoints(c['boxPoints'])
            # box = np.intp(box)
            cv2.drawContours(frame_result, [c['boxPoints']], 0, color, 3)

        # print("shape of saved_roi: ", saved_roi.shape)

        # cv2.imshow('testing', frame_result)
        # cv2.imshow('testing2', mask_road)
        # cv2.imshow('testing3', frame_cross)
        # # cv2.imshow('testing4', img_road)
        # cv2.imshow('testing4', img_general)

        # key = cv2.waitKey(300000)
        # while(1):
        #     key = cv2.waitKey(30)
        #     if key == ord('q') or key == 27:
        #         break

    # print(crosswalks)

    cv2.imwrite(str(path) + 'app/static/images/05.png', frame_result)
    # cv2.imwrite('static/images/01.png', frame_result)
    print('image saved.')

    return render_template(
        'index.html',
        title='testing',
        testing='Hello!',
        image_file='images/01.png',
        has_image=True
    )
    # cv2.imwrite(str(path) + '/assets/images/sample_bicycle_30.png', frame_hough)
    # cv2.imwrite(str(path) + '/assets/images/sample_bicycle_26.png', img_road)
    # cv2.imwrite(str(path) + '/assets/images/sample_bicycle_27.png', mask_road)
    # cv2.imwrite(str(path) + '/assets/images/sample_bicycle_28.png', frame_cross)
    # cv2.imwrite(str(path) + '/assets/images/sample_bicycle_29.png', frame_hough)


def create_app():
    app = Flask(__name__)

    @app.route('/test')
    def hello_world():
        return jsonify(msg='Hello World!')

    @app.route('/')
    def index():
        return render_template(
            'index.html',
            title='testing',
            testing='Hello!',
            image_file='images/sample.png',
            has_image=True
        )

    @app.route('/do')
    def doit():
        do_image_processing()
    # @app.route('/get_image')
    # def get_image():
    #     if Flask.request.args.get('type') == 1:
    return app
