import numpy as np
import cv2
import imutils
import random


class DataGenerator:
    def __init__(self, fonts=None, geometric=True, photometric=True):
        if fonts is None:
            fonts = ['nyala']
        self.fonts = fonts
        self.geometric = geometric
        self.photometric = photometric

    def geometric_distortion(self, image):
        # TODO: Define a geometric distortion matrix and distort
        pass

    def photometric_distortion(self, image):
        # TODO: Add photometric distortion
        pass

    @staticmethod
    def text2img(self, text, font):
        # TODO: convert text to image
        pass

    def generate_from(self, text, shape, count=1):
        images = np.zeros((count, shape))
        for c in range(count):
            font = random.choice(self.fonts)
            img = self.text2img(text, font)
            if self.geometric:
                img = self.geometric(img)
            if self.photometric:
                img = self.photometric(img)

            images[c] = img
        return images

