from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class RGB(SpellBase):
	def process(self, cv_image):
		height, width, channels = cv_image.shape
		b, g, r = cv2.split(cv_image)
		empty = np.zeros((height, width, 1), np.uint8)

		# Acquire Red, Green, Blue and Gray image
		red_img = cv2.merge((empty, empty, r))
		green_img = cv2.merge((empty, g, empty))
		blue_img = cv2.merge((b, empty, empty))

		red_texture = SpellBase.to_kivy_texture(red_img)
		green_texture = SpellBase.to_kivy_texture(green_img)
		blue_texture = SpellBase.to_kivy_texture(blue_img)

		return (red_texture, green_texture, blue_texture)
