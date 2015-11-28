from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Rotate(SpellBase):
    def process(self, cv_image, rotation):
        (oldY,oldX) = cv_image.shape[:2] #note: numpy uses (y,x) convention but most OpenCV functions use (x,y)
        M = cv2.getRotationMatrix2D((oldX/2,oldY/2), rotation, 1) #rotate about center of image.

        r = np.deg2rad(rotation)
        newX,newY = (abs(np.sin(r)*oldY) + abs(np.cos(r)*oldX),abs(np.sin(r)*oldX) + abs(np.cos(r)*oldY))

        #the warpAffine function call, below, basically works like this:
        # 1. apply the M transformation on each pixel of the original image
        # 2. save everything that falls within the upper-left "dsize" portion of the resulting image.

        #So I will find the translation that moves the result to the center of that region.
        (tx,ty) = ((newX-oldX)/2,(newY-oldY)/2)
        M[0,2] += tx #third column of matrix holds translation, which takes effect after rotation.
        M[1,2] += ty

        rotatedImg = cv2.warpAffine(cv_image, M, dsize=(int(newX),int(newY)))
        return SpellBase.to_kivy_texture(rotatedImg)
