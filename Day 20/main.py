from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

class MainWindow(MDApp):
	def builder(self):
		Screen = MDScreen()
		self.theme_cls.primary_color = "Red"
		self.label = MDLabel(text="Hello World")
		add_widget(label)
		return MDScreen


MainWindow().run()