from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label

class MainWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        label = Label(text="Hello World")

        self.add_widget(label)


class IntroApp(App):
    pass


IntroApp().run()