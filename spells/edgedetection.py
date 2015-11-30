from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

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

	def prewitt(self, cv_image, dx, dy):
		if dy>0 and dx>0:
			operator = np.matrix('\
				-2 -1  0;\
				-1  0  1;\
				 0  1  2 \
				')
		elif dy>0:
			operator = np.matrix('\
				-1  0  1;\
				-1  0  1;\
				-1  0  1 \
				')
		else:
			operator = np.matrix('\
				-1 -1 -1;\
				 0  0  0;\
				 1  1  1 \
				')
		return cv2.filter2D(cv_image, -1, operator)
