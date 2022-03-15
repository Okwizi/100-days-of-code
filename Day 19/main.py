from kivy.app import App
from kivy.uix.widget import Widget

class Interface(Widget):
	pass


class Example(App):
	def build(self):
		return Interface()


Example().run()