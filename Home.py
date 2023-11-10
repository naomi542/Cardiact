from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

class HomeScreen(Screen):
    Builder.load_file("home.kv")
