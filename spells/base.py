import cv2

class Base
    @staticmethod
    def to_kivy_texture(self, cv_image):
		buf = image.tostring()
		texture = Texture.create(size=(image.shape[1], image.shape[0]), colorfmt='bgr')
        texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
        return texture

    def load_from_file(self, source):
        return process(cv2.imread(source))

    def process(self, cv_image):
        raise NotImplementedError("Please Implement this method")
