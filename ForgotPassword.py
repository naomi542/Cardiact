from kivy.uix.screenmanager import Screen
from StoredProcedures.userdatabase import UserDatabase
from kivy.lang import Builder

class ForgotPasswordScreen(Screen):
    Builder.load_file("forgotpassword.kv")

    def submit(self):
        if self.email.text == "":
            self.error_message.text = "Please enter your email."
        elif db.get_user(self.email.text):
            self.reset_password()
        else:
            self.error_message.text = "An account with that email does not exist."

    def reset_password(self):
        self.confirmation_message.text = "An email has been sent to " + self.email.text + "!"
        self.error_message.text = ""
        self.cancel_btn.pos_hint = {"x": 0.2, "top": 0.35}
        self.cancel_btn.text = "Done"

    def back_to_login(self):
        self.reset()
        self.parent.current = "login"

    def reset(self):
        self.email.text = ""
        self.cancel_btn.pos_hint = {"x": 0.2, "top": 0.27}
        self.cancel_btn.text = "Cancel"
        self.error_message.text = ""
        self.confirmation_message.text = ""


db = UserDatabase("Database/userinfo.txt")
