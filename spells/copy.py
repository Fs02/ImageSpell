from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2

class Copy(SpellBase):
	def process(self, cv_image, source, target, size, cut = False):
		result = cv_image.copy()
		interest = cv_image[source[1]:source[1]+size[1], source[0]:source[0]+size[0]]
		if cut: result[source[1]:source[1]+size[1], source[0]:source[0]+size[0]] = (0, 0, 0)
		result[target[1]:target[1]+size[1], target[0]:target[0]+size[0]] = interest

		return SpellBase.to_kivy_texture(result)
