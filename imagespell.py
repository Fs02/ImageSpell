import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

import re
import cv2
from spells.spellbase import SpellBase
from spells.rgb import RGB
from spells.rotate import Rotate
from spells.resize import Resize
from spells.flip import Flip
from spells.sampling import Sampling
from spells.copy import Copy
from spells.quantization import Quantization
from spells.equalizehist import EqualizeHist
from spells.segmentation import Segmentation
from spells.blur import Blur
from spells.mask import Mask
from spells.edgedetection import EdgeDetection
from spells.colormap import Colormap
from spells.morphology import Morphology


class IntInput(TextInput):
	pat = re.compile('[^0-9]')

	def insert_text(self, substring, from_undo=False):
		s = re.sub(self.pat, '', substring)
		return super(IntInput, self).insert_text(s, from_undo=from_undo)


class FloatInput(TextInput):
	pat = re.compile('[^0-9]')

	def insert_text(self, substring, from_undo=False):
		pat = self.pat
		if '.' in self.text:
			s = re.sub(pat, '', substring)
		else:
			s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
		return super(FloatInput, self).insert_text(s, from_undo=from_undo)


class ActionBarWidget(ActionBar):
	pass

class MenuWidget(ScrollView):
	pass

class RotatePropertyWidget(GridLayout):
	pass

class ResizePropertyWidget(GridLayout):
	pass

class FlipPropertyWidget(GridLayout):
	pass

class SamplingPropertyWidget(GridLayout):
	pass

class CopyPropertyWidget(GridLayout):
	pass

class QuantizationPropertyWidget(GridLayout):
	pass

class EqualizeHistPropertyWidget(GridLayout):
	pass

class MaskPropertyWidget(GridLayout):
	pass

class BlurPropertyWidget(GridLayout):
	pass

class EdgeDetectionPropertyWidget(GridLayout):
	pass

class ColormapPropertyWidget(GridLayout):
	pass

class SegmentationPropertyWidget(GridLayout):
	pass

class MorphologyPropertyWidget(GridLayout):
	pass


class SingleDisplayWidget(BoxLayout):

	def update_display(self, image):
		self.ids.label.text = image[0]
		self.ids.image.texture = image[1]


class QuadDisplayWidget(BoxLayout):

	def update_display(self, top_left, top_right, bottom_left, bottom_right):
		self.ids.top_left_label.text = top_left[0]
		self.ids.top_left_image.texture = top_left[1]

		self.ids.top_right_label.text = top_right[0]
		self.ids.top_right_image.texture = top_right[1]

		self.ids.bottom_left_label.text = bottom_left[0]
		self.ids.bottom_left_image.texture = bottom_left[1]

		self.ids.bottom_right_label.text = bottom_right[0]
		self.ids.bottom_right_image.texture = bottom_right[1]


class LoadDialog(FloatLayout):
	load = ObjectProperty(None)
	cancel = ObjectProperty(None)
	mask_image = ObjectProperty(None)


class SaveDialog(FloatLayout):
	save = ObjectProperty(None)
	text_input = ObjectProperty(None)
	cancel = ObjectProperty(None)


class Root(BoxLayout):
	loadfile = ObjectProperty(None)
	savefile = ObjectProperty(None)
	text_input = ObjectProperty(None)

	def __init__(self, **kwargs):
		super(Root, self).__init__(**kwargs)

		# viewport widget
		self.single_display = SingleDisplayWidget()
		self.quad_display = QuadDisplayWidget()

		# property widget
		self.rotate_properties = RotatePropertyWidget()
		self.resize_properties = ResizePropertyWidget()
		self.flip_properties = FlipPropertyWidget()
		self.sampling_properties = SamplingPropertyWidget()
		self.copy_properties = CopyPropertyWidget()
		self.quantization_properties = QuantizationPropertyWidget()
		self.equalizehist_properties = EqualizeHistPropertyWidget()
		self.mask_properties = MaskPropertyWidget()
		self.blur_properties = BlurPropertyWidget()
		self.edgedetection_properties = EdgeDetectionPropertyWidget()
		self.colormap_properties = ColormapPropertyWidget()
		self.segmentation_properties = SegmentationPropertyWidget()
		self.morphology_properties = MorphologyPropertyWidget()

	def display_single(self, image):
		self.single_display.update_display(image)
		if self.ids.viewport.children[0] != self.single_display:
			self.ids.viewport.clear_widgets()
			self.ids.viewport.add_widget(self.single_display)

	def display_quad(self, top_left, top_right, bottom_left, bottom_right):
		self.quad_display.update_display(
			top_left, top_right, bottom_left, bottom_right)
		if self.ids.viewport.children[0] != self.quad_display:
			self.ids.viewport.clear_widgets()
			self.ids.viewport.add_widget(self.quad_display)

	def on_rotate(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
			self.ids.properties.add_widget(self.rotate_properties)
		self.rotate_properties.ids.rotation.value = 0
		self.display_single(
			('Original', SpellBase.to_kivy_texture(self.cv_image)))

	def on_rotate_update(self):
		rotation = self.rotate_properties.ids.rotation.value
		self.display_single((str(rotation) + " Degrees",
							Rotate().process(self.cv_image, rotation)))

	def on_resize(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.resize_properties)
		self.resize_properties.ids.width_scale.text = '1'
		self.resize_properties.ids.height_scale.text = '1'
		self.on_resize_update()

	def on_resize_update(self):
		width_scale = float(
			self.resize_properties.ids.width_scale.text) if self.resize_properties.ids.width_scale.text != '' else 1
		height_scale = float(
			self.resize_properties.ids.height_scale.text) if self.resize_properties.ids.height_scale.text != '' else 1

		self.display_single(("Scaled", Resize().process(
			self.cv_image, (width_scale, height_scale))))

	def on_flip(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.flip_properties)
		self.flip_properties.ids.horizontal.active = False
		self.flip_properties.ids.vertical.active = False
		self.on_flip_update()

	def on_flip_update(self):
		horizontal = self.flip_properties.ids.horizontal.active
		vertical = self.flip_properties.ids.vertical.active

		self.display_single(("Flipped", Flip().process(
			self.cv_image, horizontal, vertical)))

	def on_sampling(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.sampling_properties)
		self.sampling_properties.ids.factor.text = '5'
		self.on_sampling_update()

	def on_sampling_update(self):
		factor = int(
			self.sampling_properties.ids.factor.text) if self.sampling_properties.ids.factor.text != '' else 1

		self.display_single(
			("Sampling " + str(factor), Sampling().process(self.cv_image, factor)))

	def on_copy(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.copy_properties.ids.source_x.text = "0"
		self.copy_properties.ids.source_y.text = "0"
		self.copy_properties.ids.target_x.text = "0"
		self.copy_properties.ids.target_y.text = "0"
		self.copy_properties.ids.size_x.text = "100"
		self.copy_properties.ids.size_y.text = "100"
		self.ids.properties.add_widget(self.copy_properties)
		self.display_single(("Copy & Paste", SpellBase().to_kivy_texture(self.cv_image)))

	def on_copy_update(self, cut = False):
		source_x = int(self.copy_properties.ids.source_x.text) if self.copy_properties.ids.source_x.text != '' else 0
		source_y = int(self.copy_properties.ids.source_y.text) if self.copy_properties.ids.source_y.text != '' else 0
		target_x = int(self.copy_properties.ids.target_x.text) if self.copy_properties.ids.target_x.text != '' else 0
		target_y = int(self.copy_properties.ids.target_y.text) if self.copy_properties.ids.target_y.text != '' else 0
		size_x = int(self.copy_properties.ids.size_x.text) if self.copy_properties.ids.size_x.text != '' else 1
		size_y = int(self.copy_properties.ids.size_y.text) if self.copy_properties.ids.size_y.text != '' else 1
		self.display_single(("Copy & Paste", Copy().process(self.cv_image, (source_x, source_y), (target_x, target_y), (size_x, size_y), cut)))

	def on_quantization(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.quantization_properties)
		self.quantization_properties.ids.factor.text = '10'
		self.on_quantization_update()

	def on_quantization_update(self):
		K = int(self.quantization_properties.ids.factor.text) if self.quantization_properties.ids.factor.text != '' else 1

		self.display_single(
			("K = " + str(K), Quantization().process(self.cv_image, K)))

	def on_equalizehist(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.equalizehist_properties)
		self.display_single(
			('Equalized Histogram', EqualizeHist().process(self.cv_image)))

	def on_mask(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.mask_properties)

	def on_blur(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.blur_properties)
		self.blur_properties.ids.type.text = 'Mean'
		self.blur_properties.ids.kernel_size.value = 3
		self.on_blur_update()

	def on_blur_update(self):
		blur_type = self.blur_properties.ids.type.text
		kernel_size = int(self.blur_properties.ids.kernel_size.value)
		self.display_single((str(kernel_size) + "px " + blur_type + " filtering", Blur().process(self.cv_image, blur_type, kernel_size)))

	def on_edgedetection(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.edgedetection_properties)
		self.edgedetection_properties.ids.operator.text = 'Prewitt'
		self.edgedetection_properties.ids.kernel_size.text = '3'
		self.edgedetection_properties.ids.min_values.text = '100'
		self.edgedetection_properties.ids.max_values.text = '200'
		self.edgedetection_properties.ids.direction.text = 'North'
		self.on_edgedetection_update()

	def on_edgedetection_update(self):
		operator = self.edgedetection_properties.ids.operator.text
		kernel_size = int(self.edgedetection_properties.ids.kernel_size.text) if self.edgedetection_properties.ids.kernel_size.text != '' else 3
		min_values = int(self.edgedetection_properties.ids.min_values.text) if self.edgedetection_properties.ids.min_values.text != '' else 100
		max_values = int(self.edgedetection_properties.ids.max_values.text) if self.edgedetection_properties.ids.max_values.text != '' else 200
		direction = self.edgedetection_properties.ids.direction.text

		self.display_single((operator, EdgeDetection().process(self.cv_image, operator, kernel_size, direction, min_values, max_values)))

	def on_colormap(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.colormap_properties)
		self.colormap_properties.ids.map.text = 'Autumn'
		self.on_colormap_update()

	def on_colormap_update(self):
		colormap = self.colormap_properties.ids.map.text
		self.display_single((colormap, Colormap().process(self.cv_image, colormap)))

	def on_segmentation(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.segmentation_properties)
		self.segmentation_properties.ids.mode.text = 'Distance Transform'
		self.on_segmentation_update()

	def on_segmentation_update(self):
		distance_transform = self.segmentation_properties.ids.mode.text != 'Erosion'
		opening, unknown, markers, segmented = Segmentation().process(self.cv_image, distance_transform)
		self.display_quad(('Threshold', opening), ('Unknown', unknown), ('Markers', markers), ('Segmented', segmented))

	def on_morphology(self):
		if not hasattr(self, 'cv_image'):
			return
		if len(self.ids.properties.children) > 0:
			self.ids.properties.clear_widgets()
		self.ids.properties.add_widget(self.morphology_properties)
		self.morphology_properties.ids.operation.text = 'Erosion'
		self.morphology_properties.ids.kernel.text = 'Uniform'
		self.morphology_properties.ids.kernel_size.value = 3
		self.on_morphology_update()

	def on_morphology_update(self):
		operation = self.morphology_properties.ids.operation.text
		kernel = self.morphology_properties.ids.kernel.text
		kernel_size = self.morphology_properties.ids.kernel_size.value
		title = str(kernel_size) + 'x' + str(kernel_size) + ' ' + kernel + ' ' + operation
		self.display_single((title, Morphology().process(self.cv_image, operation, kernel, kernel_size)))

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load_mask(self):
		content = LoadDialog(load=self.load_mask, cancel=self.dismiss_popup, mask_image=True)
		self._popup = Popup(title="Load file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	def load_mask(self, path, filename, mask_image):
		if len(filename) > 0 and mask_image:
			cv_image_mask = cv2.imread(filename[0], 0)
			self.display_single(('Mask', Mask().process(self.cv_image, cv_image_mask)))
		self.dismiss_popup()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup, mask_image=False)
		self._popup = Popup(title="Load file", content=content,
							size_hint=(0.9, 0.9))
		self._popup.open()

	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename, mask_image):
		if len(filename) > 0 and not mask_image:
			self.cv_image = cv2.imread(filename[0])
			original = SpellBase.to_kivy_texture(self.cv_image)
			red, green, blue = RGB().process(self.cv_image)
			self.display_quad(('Original', original), ('Red', red), ('Green', green), ('Blue', blue))
		self.dismiss_popup()

	def save(self, path, filename):
		# with open(os.path.join(path, filename), 'w') as stream:
		#    stream.write(self.text_input.text)

		self.dismiss_popup()


class ImageSpellApp(App):
	pass

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == "__main__":
	ImageSpellApp().run()
