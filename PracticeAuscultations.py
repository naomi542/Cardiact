from kivy.uix.screenmanager import Screen
from kivy.uix.dropdown import DropDown
from kivy.lang import Builder
from kivy.logger import Logger
import sounddevice as sd
import scipy.io.wavfile as wavf
from playsound import playsound


class PracticeAuscultationsScreen(Screen):
    Builder.load_file("practiceauscultations.kv")
    string_recording_name = 'test'
    string_selected_locatons = []
    counter=0

    def accept_variables(self, recording_name, selected_locations):
        Logger.info(recording_name)
        Logger.info(selected_locations)
        PracticeAuscultationsScreen.string_recording_name = recording_name
        PracticeAuscultationsScreen.string_selected_locatons = selected_locations

       # PracticeAuscultationsScreen.location.text = PracticeAuscultationsScreen.string_selected_locatons[PracticeAuscultationsScreen.counter]
        #PracticeAuscultationsScreen.rec_name.text = PracticeAuscultationsScreen.string_recording_name

    def recordSound(self, name, seconds):
        fs = 44100  # Sample rate
        duration = seconds  # Duration of recording

        myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=2)
        sd.wait()

        sd.play(myrecording, fs)
        sd.wait()

        directory = "../261 Cardiact/TestSounds/"
        wavf.write(directory + name + '.wav', fs, myrecording)

    def setVariables(self):
        self.location.text = self.string_selected_locatons[self.counter]
        self.rec_name.text = self.string_recording_name

    def doRecording(self):
        saved_name= self.string_recording_name + self.string_selected_locatons[self.counter]
        time = self.select_timer.text
        time = int(time[:-1])
        self.recordSound(saved_name, time)

    def redoRecording(self):
        self.doRecording()

    def playRecording(self):
        saved_name= self.string_recording_name + self.string_selected_locatons[self.counter]
        directory = "../261 Cardiact/TestSounds/{}.wav".format(saved_name)
        playsound(directory)

    def nextRecording(self):
        self.counter = self.counter + 1
        self.setVariables()

