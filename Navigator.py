from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

from Login import LoginScreen
from Home import HomeScreen
from CreateAccount import CreateAccountScreen
from AuscultationResults import AuscultationResultsScreen
from ForgotPassword import ForgotPasswordScreen
from NewAuscultation import NewAuscultationScreen
from SendingEmail.Emailing import EmailLoginScreen, EmailScreen
from PracticeAuscultations import PracticeAuscultationsScreen
from AuscultationHistory import AuscultationHistoryScreen
from Quizzes import QuizzesScreen
from BeginnerQuiz import BeginnerQuizScreen
from Help import HelpScreen

class WindowManager(ScreenManager):
    pass

class LoginScreen(LoginScreen):
    pass

class HomeScreen(HomeScreen):
    pass

class AuscultationResultsScreen(AuscultationResultsScreen):
    pass

class CreateAccountScreen(CreateAccountScreen):
    pass

class ForgotPasswordScreen(ForgotPasswordScreen):
    pass

class NewAuscultationScreen(NewAuscultationScreen):
    pass

class EmailLoginScreen(EmailLoginScreen):
    pass

class EmailScreen(EmailScreen):
    pass

class PracticeAuscultationsScreen(PracticeAuscultationsScreen):
    pass

class AuscultationHistoryScreen(AuscultationHistoryScreen):
    pass

class QuizzesScreen(QuizzesScreen):
    pass

class BeginnerQuizScreen(BeginnerQuizScreen):
    pass

class HelpScreen(HelpScreen):
    pass

Window.size = (360,600)
navigator = Builder.load_file("navigator.kv")

class Cardiact(App):
    def build(self):
        return navigator

if __name__ == "__main__":
    Cardiact().run()
    print("ran")