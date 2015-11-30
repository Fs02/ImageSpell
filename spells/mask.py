from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2

class Mask(SpellBase):
	def process(self, cv_image, cv_mask_image):
		return SpellBase.to_kivy_texture(cv2.bitwise_and(cv_image, cv_image, mask = cv_mask_image))
