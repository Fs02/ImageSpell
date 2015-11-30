from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2

class EqualizeHist(SpellBase):
	def process(self, cv_image):
		result = cv_image.copy()
		result[:, :, 0] = cv2.equalizeHist(cv_image[:, :, 0])

		return SpellBase.to_kivy_texture(result)
