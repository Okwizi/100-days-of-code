from kivy.app import App
from kivy.uix.label import Label

class Example(App):
	def build(self):
		return Label(text="Hello World ;)")


Example().run()
