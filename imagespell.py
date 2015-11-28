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
from kivy.graphics.texture import Texture
import cv2

class ActionBarWidget(ActionBar):
	pass

class MenuWidget(ScrollView):
	pass

class QuadImageWidget(BoxLayout):
	pass

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
		buf = img.tostring()
		texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='bgr')
		texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
		self.ids.quad_display.ids.top_left_image.texture = texture
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
