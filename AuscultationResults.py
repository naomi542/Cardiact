from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout


class SavedRecordingsDropDown(BoxLayout):
    pass


class AuscultationResultsScreen(Screen):
    Builder.load_file("auscultationresults.kv")



