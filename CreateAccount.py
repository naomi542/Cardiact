from kivy.uix.screenmanager import Screen
from StoredProcedures.userdatabase import UserDatabase
from kivy.lang import Builder

class CreateAccountScreen(Screen):
    Builder.load_file("createaccount.kv")

    def submit(self):
        if self.validate_input():
            if db.add_user(self.firstname.text, self.lastname.text, self.email.text, self.password.text):
                self.reset()
                self.parent.current = "home"
            else:
                self.error_message.text = "An account with this email already exists"

    def cancel(self):
        self.reset()
        self.parent.current = "login"

    def validate_input(self):
        if(self.firstname.text == ""  or self.lastname.text == "" or self.email.text == "" or self.password.text == "" or self.confirm_password.text
                == ""):
            self.error_message.text = "Please fill in all fields"
            return False
        elif(self.password.text != self.confirm_password.text):
            self.error_message.text = "Passwords do not match"
            self.password.text = ""
            self.confirm_password.text = ""
            return False
        else:
            return True

    def reset(self):
        self.firstname.text = ""
        self.lastname.text = ""
        self.email.text = ""
        self.password.text = ""
        self.confirm_password.text = ""
        self.error_message.text = ""

db = UserDatabase("Database/userinfo.txt")
