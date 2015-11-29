from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Morphology(SpellBase):
    def process(self, cv_image, operation = 'Erosion', kernel_type = 'Uniform', kernel_size = 3):
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        kernel = None
        if kernel_type == 'Rect':
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(kernel_size, kernel_size))
        elif kernel_type == 'Ellipse':
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(kernel_size, kernel_size))
        elif kernel_type == 'Cross':
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(kernel_size, kernel_size))
        else:
            kernel = np.ones((kernel_size, kernel_size), np.uint8)

        return {
            'Erosion': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.erode(gray, kernel, iterations = 1),cv2.COLOR_GRAY2RGB)),
            'Dilation': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.dilate(gray, kernel, iterations = 1),cv2.COLOR_GRAY2RGB)),
            'Opening': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel),cv2.COLOR_GRAY2RGB)),
            'Closing': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel),cv2.COLOR_GRAY2RGB)),
            'Gradient': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.morphologyEx(gray, cv2.MORPH_GRADIENT, kernel),cv2.COLOR_GRAY2RGB)),
            'Top Hat': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.morphologyEx(gray, cv2.MORPH_TOPHAT, kernel),cv2.COLOR_GRAY2RGB)),
            'Black Hat': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel),cv2.COLOR_GRAY2RGB))
        }[operation]
