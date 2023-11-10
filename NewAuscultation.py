from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox
from kivy.logger import Logger
from PracticeAuscultations import PracticeAuscultationsScreen

class NewAuscultationScreen(Screen):
    Builder.load_file("newauscultation.kv")

    def submit(self):
        selected_locations = self.check_selected_locations()
        PracticeAuscultationsScreen.accept_variables(self, self.recording_name.text, selected_locations)
        self.parent.current = "practiceauscultations"

    def cancel(self):
        self.reset()
        self.parent.current = "home"

    def check_selected_locations(self):
        selected_locations = []
        for key, val in self.ids.items():
            try:
                if self.ids[key].active is True:
                    selected_locations.append(key)
            except:
                continue
        return selected_locations

    def reset(self):
        self.recording_name.text = ""
        for key, val in self.ids.items():
            try:
                self.ids[key].active = False
            except:
                continue
