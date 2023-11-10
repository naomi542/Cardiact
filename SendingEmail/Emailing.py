### g-mail lib
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# kivy lib
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen, ScreenManager
from SendingEmail.EmailDataBase import EmailDataBase
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout


class EmailLoginScreen(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)

    def loginBtn(self):
        if db.validate(self.email.text, self.password.text):
            EmailScreen.current = self.email.text
            self.reset()
            self.parent.current = "email"
        else:
            invalidLogin()

    def reset(self):
        self.email.text = ""
        self.password.text = ""


class EmailScreen(Screen):
    current = ""
    file_path = StringProperty("No file chosen")
    the_popup = ObjectProperty(None)
    message = StringProperty()

    def open_popup(self):
        self.the_popup = FileChoosePopup(load=self.load)
        self.the_popup.open()

    def load(self, selection):
        self.file_path = str(selection[0])
        self.the_popup.dismiss()
        print(self.file_path)

        # check for non-empty list i.e. file selected
        if self.file_path:
            self.ids.get_file.text = self.file_path

    # send Function
    def send(self):
        file = open("SendingEmail/email_users.txt", "r")
        user = file.readline().rstrip("\n")
        sender = (user.split(";", 1)[0])
        pas = (user.split(";", 2)[1])
        receiver = self.ids.tosend.text
        subject = self.ids.sub.text
        body = self.ids.body.text
        filename = self.file_path
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = receiver
        msg['Subject'] = subject

        if receiver == "":
            self.message = "Recipient Required"
            return

        if body == "" and filename == "No file chosen":
            self.message = "Message Required"
            return

        msg.attach(MIMEText(body, 'plain'))
        if (filename != "No file chosen"):
            attachment = open(filename, 'rb')
            part = MIMEBase('application', 'octet-stream')
            part.set_payload((attachment).read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= " + filename)
            msg.attach(part)
        else:
            pass

        text = msg.as_string()
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, pas)

        server.sendmail(sender, receiver, text)
        server.quit()
        self.message = "Sent!"
        self.reset()

    def reset(self):
        self.ids.tosend.text = ""
        self.ids.sub.text = ""
        self.ids.body.text = ""
        self.file_path = ""

class FileChoosePopup(Popup):
    load = ObjectProperty()


def invalidLogin():
    pop = Popup(title='Invalid Login',
                content=Label(text='Invalid username or password.'),
                size_hint=(0.85, 0.85))
    pop.open()


kv = Builder.load_file("SendingEmail/email.kv")

db = EmailDataBase("SendingEmail/email_users.txt")
