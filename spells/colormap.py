from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Colormap(SpellBase):
	def process(self, cv_image, map = 'Autumn'):
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		return {
			'Autumn': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_AUTUMN)),
			'Bone': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_BONE)),
			'Jet': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_JET)),
			'Winter': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_WINTER)),
			'Rainbow': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_RAINBOW)),
			'Ocean': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_OCEAN)),
			'Summer': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_SUMMER)),
			'Spring': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_SPRING)),
			'Cool': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_COOL)),
			'HSV': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_HSV)),
			'Pink': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_PINK)),
			'Hot': SpellBase.to_kivy_texture(cv2.applyColorMap(gray, cv2.COLORMAP_HOT))
		}[map]
