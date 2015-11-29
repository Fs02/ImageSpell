from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Flip(SpellBase):
    def process(self, cv_image, horizontal, vertical):
        if horizontal and vertical:
            return SpellBase.to_kivy_texture(cv2.flip(cv_image,-1))
        if horizontal == True:
            return SpellBase.to_kivy_texture(cv2.flip(cv_image,1))
        if vertical == True:
            return SpellBase.to_kivy_texture(cv2.flip(cv_image,0))

        return SpellBase.to_kivy_texture(cv_image)
