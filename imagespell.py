import kivy
kivy.require('1.9.0')

from kivy.app import App

from kivy.uix.actionbar import ActionBar
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView

class ActionBarWidget(ActionBar):
	pass

class MenuWidget(ScrollView):
	pass

class QuadImageWidget(BoxLayout):
	pass

class RootWidget(BoxLayout):
	pass

class ImageSpellApp(App):
	def build(self):
		return RootWidget()

if __name__ == "__main__":
	ImageSpellApp().run()
