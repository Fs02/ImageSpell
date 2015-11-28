import cv2
from kivy.graphics.texture import Texture

class SpellBase(object):
    @staticmethod
    def to_kivy_texture(cv_image):
        flipped = cv2.flip(cv_image, 0)
        buf = flipped.tostring()
        texture = Texture.create(size=(cv_image.shape[1], cv_image.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture

    def load_from_file(self, source):
        return process(cv2.imread(source))

    def process(self, cv_image):
        raise NotImplementedError("Please Implement this method")
