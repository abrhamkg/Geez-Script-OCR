# -*- coding: utf-8 -*-
"""
Created on Fri Dec 20 16:26:35 2019

@author: abrih
"""

import numpy as np
import cv2
from imutils.object_detection import non_max_suppression
import matplotlib.pyplot as plt
import configparser
import os
import logging
import config


settings = configparser.ConfigParser()
settings.read('config.ini')

MODEL_DIR, DATA_DIR, DEBUG = config.parse_config(settings, 'DEFAULT', ['MODEL_DIR', 'DATA_DIR', 'MODE'])

layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]


class Detector(object):
    def detect(image):
        raise NotImplementedError

    @staticmethod
    def draw_boxes(image, boxes):
        raise NotImplementedError


class EASTDetector(Detector):
    net = cv2.dnn.readNet(os.path.join(MODEL_DIR, "frozen_east_text_detection.pb"))

    def __init__(self):
        super().__init__()

    def detect(image):
        min_confidence = 0.1
        (H, W) = image.shape[:2]
        H, W = (W//32) * 32, (H//32) * 32
        image = cv2.resize(image, (H, W))
        blob = cv2.dnn.blobFromImage(image, 1.0, (W, H),(123.68, 116.78, 103.94), 
                                     swapRB=True, crop=False)
        EASTDetector.net.setInput(blob)
        (scores, geometry) = EASTDetector.net.forward(layerNames)
        
        (numRows, numCols) = scores.shape[2:4]
        
        rects = []
        confidences = []
        
        for y in range(0, numRows):
            scoresData = scores[0,0,y]
            
            xData0 = geometry[0, 0, y]
            xData1 = geometry[0, 1, y]
            xData2 = geometry[0, 2, y]
            xData3 = geometry[0, 3, y]
            anglesData = geometry[0, 4, y]
            
            for x in range(0, numCols):
                if scoresData[x] < min_confidence:
                    continue
                (offsetX, offsetY) = (x * 4.0, y*4.0)
                angle = anglesData[x]
                cos = np.cos(angle)
                sin = np.sin(angle)
                
                h = xData0[x] + xData2[x]
                w = xData1[x] + xData3[x]
                
                endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
                endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
                
                startX = int(endX - w)
                startY = int(endY - h)
                
                rects.append((startX, startY, endX, endY))
                confidences.append(scoresData[x])
                
        boxes = non_max_suppression(np.array(rects), probs=confidences)
        return boxes, image

    @staticmethod
    def draw_boxes(image, boxes):
        for (startX, startY, endX, endY) in boxes:
            cv2.rectangle(image, (startX, startY), (endX, endY), (0,255,0), 2)


class MSERDetector(Detector):
    mser = cv2.MSER_create(_delta=4, _min_area=20, _max_variation=0.25)

    def __init__(self):
        super().__init__()

    def detect(image, kernel=None):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
        if DEBUG:
            plt.imshow(thresh, cmap='gray')
            plt.figure()
        if kernel is None:
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 5))

        filtered = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
        if DEBUG:
            plt.imshow(filtered, cmap='gray')

        regions, bboxes = MSERDetector.mser.detectRegions(filtered)
        hulls = [cv2.convexHull(p.reshape(-1, 1, 2)) for p in regions]
        lines = MSERDetector.identify_lines(bboxes)

        return bboxes, hulls

    @staticmethod
    def identify_lines(bboxes):

        bboxes = sorted(bboxes, key=lambda g: (g[1], g[0]))
        lines = []
        ptr = 0
        logging.log(logging.INFO, " Started line identification")
        while True:
            if ptr >= len(bboxes):
                break
            line = [bboxes[ptr]]
            top_average = line[0][1]
            count = 1
            ptr += 1
            while ptr < len(bboxes) and abs((bboxes[ptr][1] - top_average)/top_average) < 0.5:
                logging.log(logging.INFO, "Working on {}".format(ptr))
                top_average = ((top_average * count) + bboxes[ptr][1]) / (count + 1)
                count += 1
                line.append(bboxes[ptr])
                ptr += 1
            logging.log(logging.INFO, " Detected one line")
            # ptr -= 1
            lines.append(line)
        logging.log(logging.INFO, " Finished detecting lines")
        return lines

    @staticmethod
    def draw_boxes(image, bboxes=None, hulls=None):
        if bboxes is None and hulls is None:
            raise ValueError("One of bboxes or hulls must be specified")
        if bboxes is not None:
            for bbox in bboxes:
                (startX, startY, W, H) = bbox
                endX, endY = startX + W, startY + H
                cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0),1)
                #print(bbox)
        else:
            cv2.polylines(image, hulls, 1, (0, 255, 0))


if __name__ == '__main__':
    IMG_TRAIN_DIR = os.path.join(DATA_DIR, 'img/train')
    image = cv2.imread(os.path.join(IMG_TRAIN_DIR, 'image_1.png'))
    detector = MSERDetector
    boxes, hulls = detector.detect(image)
    detector.draw_boxes(image, hulls=hulls, bboxes=boxes)
    plt.figure()
    plt.imshow(image)
    plt.show()
