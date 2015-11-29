from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Quantization(SpellBase):
    def process(self, cv_image, K):
        Z = cv_image.reshape((-1, 3))

        # convert to np.float32
        Z = np.float32(Z)

        # define criteria, number of clusters(K) and apply kmeans()
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        ret, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_PP_CENTERS)

        # Convert bake to uint8 and make original image
        center = np.uint8(center)
        res = center[label.flatten()]
        res2 = res.reshape((cv_image.shape))

        return SpellBase.to_kivy_texture(res2)
