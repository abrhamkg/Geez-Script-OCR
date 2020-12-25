import numpy as np
import cv2
import detector
import configparser
import os
import copy
# from tqdm import tqdm

config = configparser.ConfigParser()
config.read('config.ini')

EXPT_FOLDER = 'experiments'
MODEL_DIR = config['DEFAULT']['MODEL_DIR']
DATA_DIR = config['DEFAULT']['DATA_DIR']

if __name__ == '__main__':
    IMG_TRAIN_DIR = os.path.join(DATA_DIR, 'img/train')
    name = 'image_1.png'
    image = cv2.imread(os.path.join(IMG_TRAIN_DIR, name))
    detector = detector.MSERDetector
    ktypes = ['RECT', 'CROSS', 'ELLIPSE']
    settings = [(k, i, j) for k in ktypes for i in range(1, 12) for j in range(1, 12)]

    for kernel, x, y in settings:
        img_cpy = copy.deepcopy(image)
        ktype = cv2.MORPH_RECT
        if kernel == 'RECT':
            ktype = cv2.MORPH_RECT
        elif kernel == 'CROSS':
            ktype = cv2.MORPH_CROSS
        elif kernel == 'ELLIPSE':
            ktype = cv2.MORPH_ELLIPSE
        
        kernel = cv2.getStructuringElement(ktype, (x, y))
        boxes, hulls = detector.detect(image, kernel)
        detector.draw_boxes(img_cpy, hulls=hulls, bboxes=boxes)
        cv2.imwrite(os.path.join(EXPT_FOLDER, '{}_{}_{}_{}.png'.format(name, ktype, x, y)), img_cpy)

