from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from StoredProcedures.auscultationhistorydatabase import AuscultationHistoryDatabase


class AuscultationHistoryScreen(Screen):
    Builder.load_file("auscultationhistory.kv")

    def on_enter(self):
        table_layout = self.create_table()
        self.ids.datatable.add_widget(table_layout)

    def get_history(self, flagged):
        if flagged:
            return db.get_flagged_auscultations()
        else:
            return db.get_auscultations()

    def create_table(self):
        table = GridLayout(cols=2)
        auscultations = self.get_history(False)
        for key in auscultations:
            table.add_widget(Label(text=key, font_size=14))
            table.add_widget(Label(text=auscultations[key][0], font_size=14))
        return table

db = AuscultationHistoryDatabase("Database/auscultationhistory.txt")

