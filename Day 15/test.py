from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.button import Button


class StackLayoutEx(StackLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        button = Button(text="test")
        self.add_widget(button)

class TestApp(App):
    pass


TestApp().run()
