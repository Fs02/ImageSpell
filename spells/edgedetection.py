from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np
from scipy.signal import convolve2d
import math

def padding_zeros(vector, pad_width, iaxis, kwargs):
	vector[:pad_width[0]] = 0
	vector[-pad_width[1]:] = 0
	return vector

class EdgeDetection(SpellBase):
	def process(self, cv_image, mode = 'Prewitt', kernel_size = 3, direction = 'Both', canny_min = 100, canny_max = 200):
		if direction == 'Horizontal':
			dx = 1
			dy = 0
		elif direction == 'Vertical':
			dx = 0
			dy = 1
		else:
			dx = 1
			dy = 1

		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		smoothed = cv2.GaussianBlur(gray,(5,5),0)
		return {
			'Prewitt': SpellBase.to_kivy_texture(cv2.cvtColor(self.prewitt(smoothed, dx, dy),cv2.COLOR_GRAY2RGB)),
			'Sobel': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.Sobel(smoothed, cv2.CV_8U, dx, dy, ksize=kernel_size),cv2.COLOR_GRAY2RGB)),
			'Canny': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.Canny(smoothed,canny_min, canny_max),cv2.COLOR_GRAY2RGB)),
			'Laplacian': SpellBase.to_kivy_texture(cv2.cvtColor(cv2.Laplacian(smoothed, cv2.CV_8U),cv2.COLOR_GRAY2RGB)),
			'Prewitt 2': SpellBase.to_kivy_texture(cv2.GaussianBlur(cv_image,(kernel_size,kernel_size),0)),
		}[mode]

	def prewitt(self, gray_image, dx, dy):
		# Construct the mask
		kx = np.matrix('\
			-1 -1 -1;\
			 0  0  0;\
			 1  1  1 \
			') / 6.0

		ky = np.matrix('\
			-1  0  1;\
			-1  0  1;\
			-1  0  1 \
			') / 6.0

		# Convolute
		gx = convolve2d(gray_image, kx, 'same')
		gy = convolve2d(gray_image, ky, 'same')

		height,width = gray_image.shape[:2]
		result = gray_image.copy()
		max_p = 0
		for y in range(0, height):
			for x in range(0, width):
				result[y,x] = math.sqrt(gx[y,x]**2 + gy[y,x]**2)
				max_p = max(max_p, result[y,x])

		print np.uint8(result > 0.08995 * max_p) * 255
		return np.uint8(result > 0.08995 * max_p) * 255
