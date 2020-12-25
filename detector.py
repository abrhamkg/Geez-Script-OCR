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

config = configparser.ConfigParser()
config.read('config.ini')

MODEL_DIR = config['DEFAULT']['MODEL_DIR']
DATA_DIR = config['DEFAULT']['DATA_DIR']

layerNames = [
    "feature_fusion/Conv_7/Sigmoid",
    "feature_fusion/concat_3"]


class Detector(object):
    def detect(image):
        raise NotImplementedError

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

    def draw_boxes(image, boxes):
        for (startX, startY, endX, endY) in boxes:
            cv2.rectangle(image, (startX, startY), (endX, endY), (0,255,0), 2)     


class MSERDetector(Detector):
    mser = cv2.MSER_create(_delta=4, _min_area=20, _max_variation=0.25)

    def __init__(self):
        super().__init__()

    def detect(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV|cv2.THRESH_OTSU)
        plt.imshow(thresh, cmap='gray')
        plt.figure()
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,10))
        #plt.imshow(kernel*255, cmap='gray')
        #plt.figure()
        filtered = cv2.morphologyEx(thresh, cv2.MORPH_DILATE, kernel)
        plt.imshow(filtered, cmap='gray')
        #filtered = gray
        #filtered = cv2.medianBlur(gray, 3)
        #cv2.imshow("www", gray)
        #cv2.waitKey(0)
        #vis = image.copy()
        #cv2.closing()
        #kernel = cv2.getStructuringElement()
        #closing = cv2.MorphologyEx(thresh, cv2.MORPH_CLOSE, )
        regions, bboxes = MSERDetector.mser.detectRegions(filtered)
        hulls = [cv2.convexHull(p.reshape(-1,1,2)) for p in regions]
        
        return bboxes, hulls

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
    detector.draw_boxes(image,hulls=hulls, bboxes=boxes)
    plt.figure()
    plt.imshow(image)
    plt.show()

    #cv2.imshow("win", image)
    #cv2.waitKey(0)