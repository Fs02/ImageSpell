from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Resize(SpellBase):
    def process(self, cv_image, scale):
        height, width = cv_image.shape[:2]
        resized = cv2.resize(cv_image, (int(scale[0]*width), int(scale[1]*height)))

        return SpellBase.to_kivy_texture(resized)
