from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

def padding_zeros(vector, pad_width, iaxis, kwargs):
	vector[:pad_width[0]] = 0
	vector[-pad_width[1]:] = 0
	return vector

class Blur(SpellBase):
	def process(self, cv_image, mode = 'Mean', kernel_size = 3):
		return {
			'Mean': SpellBase.to_kivy_texture(cv2.blur(cv_image,(kernel_size, kernel_size))),
			'Median': SpellBase.to_kivy_texture(cv2.medianBlur(cv_image,kernel_size)),
			'Mode': SpellBase.to_kivy_texture(self.modeBlur(cv_image,kernel_size)),
			'Gaussian': SpellBase.to_kivy_texture(cv2.GaussianBlur(cv_image,(kernel_size,kernel_size),0))
		}[mode]

	def modeBlur(self, cv_image, kernel_size):
		# ensure kernel size >= 3
		kernel_size = max(3, kernel_size)
		# ensure kernel size is odd
		if kernel_size % 2 == 0: kernel_size += 1

		# add padding
		padding = kernel_size/2
		b, g, r = cv2.split(cv_image)

		# perform operation per channels and return the result
		return cv2.merge((self.__modeOperation(b, padding), self.__modeOperation(g, padding), self.__modeOperation(r, padding)))

	def __modeOperation(self, cv_image, padding):
		pad_image = np.pad(cv_image, padding, padding_zeros)
		result = cv_image.copy()
		for x in range(padding, pad_image.shape[0]-padding):
			for y in range(padding, pad_image.shape[1]-padding):
				neighbord = pad_image[x-padding:x+padding+1, y-padding:y+padding+1].flatten()
				result[x-padding, y-padding] = np.bincount(neighbord).argmax()
		return result
