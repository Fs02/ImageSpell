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
	def process(self, cv_image, mode = 'Prewitt', kernel_size = 3, direction = 'North', canny_min = 100, canny_max = 200):
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		smoothed = cv2.GaussianBlur(gray,(5,5),0)
		edge = {
			'Prewitt': self.prewitt(smoothed),
			'Sobel': cv2.equalizeHist(cv2.Sobel(smoothed, cv2.CV_8U, 1, 1, ksize=kernel_size)),
			'Canny': cv2.Canny(smoothed,canny_min, canny_max),
			'Laplacian': cv2.equalizeHist(cv2.Laplacian(smoothed, cv2.CV_8U)),
			'Prewitt Compass': self.prewitt2(smoothed, direction),
		}[mode]

		return SpellBase.to_kivy_texture(cv2.cvtColor(edge, cv2.COLOR_GRAY2RGB))

	def prewitt(self, gray_image):
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

		return np.uint8(result > 0.08995 * max_p) * 255

	def prewitt2(self, gray_image, direction):
		kernel = {
			'North': np.matrix('-1 -1 -1; 1 -2 1; 1 1 1'),
			'North East': np.matrix('1 -1 -1; 1 -2 -1; 1 1 1'),
			'East': np.matrix('1 1 -1; 1 -2 -1; 1  1 -1'),
			'South East': np.matrix('1 1 1; 1 -2 -1; 1 -1 -1'),
			'South': np.matrix('1 1 1; 1 -2 1; -1 -1 -1'),
			'South West': np.matrix('1 1 1; -1 -2 1; -1 -1 1'),
			'West': np.matrix('-1 1 1; -1 -2 1; -1 1 1'),
			'North West': np.matrix('-1 -1 1; -1 -2 1; 1 1 1')
		}[direction]

		g = convolve2d(gray_image, kernel)
		return np.uint8(g)
