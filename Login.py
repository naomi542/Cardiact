from kivy.logger import Logger
from kivy.uix.screenmanager import Screen
from StoredProcedures.userdatabase import UserDatabase
from kivy.lang import Builder


class LoginScreen(Screen):
    Builder.load_file("login.kv")

    def reset(self):
        self.email.text = ""
        self.password.text = ""

    def login(self):
        if db.login(self.email.text, self.password.text):
            Logger.info("Logged in")
            self.reset()
            self.parent.current = "home"

    def create_account(self):
        self.reset()
        self.parent.current = "createaccount"

    def forgot_password(self):
        self.reset()
        self.parent.current = "forgotpassword"


db = UserDatabase("Database/userinfo.txt")
