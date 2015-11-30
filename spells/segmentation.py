from spellbase import SpellBase
from kivy.graphics.texture import Texture
import cv2
import numpy as np

class Segmentation(SpellBase):
	# http://docs.opencv.org/master/d3/db4/tutorial_py_watershed.html
	def process(self, cv_image, do_separate=True):
		# Thresholding
		gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
		ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

		# Noise removal
		kernel = np.ones((3,3), np.uint8)
		opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

		# Sure background area
		sure_bg = cv2.dilate(opening, kernel, iterations=3)

		# Finding sure foreground area
		sure_fg = None
		if do_separate:
			dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
			ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)
		else:
			sure_fg = cv2.erode(opening, kernel, iterations=2)

		# Finding unknown region
		sure_fg = np.uint8(sure_fg)
		unknown = cv2.subtract(sure_bg, sure_fg)

		# Marker labelling
		ret, markers = cv2.connectedComponents(sure_fg)

		# Add one to all labels so that sure background is not 0 but 1
		markers = markers+1

		# Now mark the region of unknown with zero
		markers[unknown==255] = 0

		# Apply watershed
		result = cv_image.copy()
		markers = cv2.watershed(cv_image, markers)
		result[markers == -1] = [255, 0, 0]

		return (SpellBase.to_kivy_texture(cv2.cvtColor(opening,cv2.COLOR_GRAY2RGB)),
				SpellBase.to_kivy_texture(cv2.cvtColor(unknown,cv2.COLOR_GRAY2RGB)),
				SpellBase.to_kivy_texture(cv2.applyColorMap(cv2.convertScaleAbs(markers), cv2.COLORMAP_JET)),
				SpellBase.to_kivy_texture(result))
