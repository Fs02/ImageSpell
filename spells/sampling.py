from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Sampling(SpellBase):
    def process(self, cv_image, factor):
        height,width = cv_image.shape[:2]
        sampled = cv_image.copy()

        for y in range(0, height):
            for x in range(0, width):
                sampled[y, x] = cv_image[y - y % factor, x - x % factor]

        return SpellBase.to_kivy_texture(sampled)
