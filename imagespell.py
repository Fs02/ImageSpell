import kivy
kivy.require('1.9.0')

from kivy.app import App
from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.floatlayout import FloatLayout
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

import cv2
from spells.spellbase import SpellBase
from spells.rgb import RGB

class ActionBarWidget(ActionBar):
	pass

class MenuWidget(ScrollView):
	pass

class QuadImageWidget(BoxLayout):
	def update_display(self, top_left, top_right, bottom_left, bottom_right):
		self.ids.top_left_image.texture = top_left
		self.ids.top_right_image.texture = top_right
		self.ids.bottom_left_image.texture = bottom_left
		self.ids.bottom_right_image.texture = bottom_right

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SaveDialog(FloatLayout):
    save = ObjectProperty(None)
    text_input = ObjectProperty(None)
    cancel = ObjectProperty(None)

class Root(BoxLayout):
	loadfile = ObjectProperty(None)
	savefile = ObjectProperty(None)
	text_input = ObjectProperty(None)

	def dismiss_popup(self):
		self._popup.dismiss()

	def show_load(self):
		content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
		self._popup = Popup(title="Load file", content=content,
                            size_hint=(0.9, 0.9))
		self._popup.open()

	def show_save(self):
		content = SaveDialog(save=self.save, cancel=self.dismiss_popup)
		self._popup = Popup(title="Save file", content=content, size_hint=(0.9, 0.9))
		self._popup.open()

	def load(self, path, filename):
		img = cv2.imread(filename[0])
		original = SpellBase.to_kivy_texture(img)
		red, green, blue = RGB().process(img)
		self.ids.quad_display.update_display(original, red, green, blue)
		self.dismiss_popup()

	def save(self, path, filename):
        #with open(os.path.join(path, filename), 'w') as stream:
        #    stream.write(self.text_input.text)

		self.dismiss_popup()


class ImageSpellApp(App):
	pass

Factory.register('Root', cls=Root)
Factory.register('LoadDialog', cls=LoadDialog)
Factory.register('SaveDialog', cls=SaveDialog)

if __name__ == "__main__":
	ImageSpellApp().run()
