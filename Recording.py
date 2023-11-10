import sounddevice as sd
import soundfile as sf
import scipy
import os
import os.path
import scipy.io.wavfile as wavf


"""
param: name of auscultation
param: seconds of recording
future param: name of file to save sound to?
"""
def recordSound (filename, location, seconds):

    fs = 44100 #Sample rate
    duration = seconds #Duration of recording

    # making a new recording
    #int recarray = int(duration*fs)
    myrecording = sd.rec(int(duration*fs), samplerate=fs, channels=2)
    sd.wait()

    sd.play(myrecording, fs)
    sd.wait()

    # Saving as wav file
    # write(name, fs, myrecording) #save as .wav file
    #directory = "../261 Cardiact/TestSounds"
    #wavf.write(directory+name+'.wav', fs, myrecording)

    #myrecording, fs = sf.read('newaudio.wav')

    pathWant = os.path.join("../Cardiact/TestSounds/" + filename)

    # check to see if file already exists
    if os.path.exists(pathWant):
        wavf.write(pathWant+location+'.wav', fs, myrecording)
    else:
        os.mkdir(pathWant)
        wavf.write(pathWant+location+'.wav', fs, myrecording)

    #print(pathWant)
#recordSound(nameOfAuscultation, numberOfSeconds)
recordSound('auscultation/', 'aorta3', 3)

## USE THE BELOW FOR PRACTICEAUSCULTATIONS
############################################
pathWant = os.path.join("../Cardiact/TestSounds/" + self.recording_name)

# check to see if file already exists
if os.path.exists(pathWant):
    wavf.write(pathWant + self.string_selected_locatons + '.wav', fs, myrecording)
else:
    os.mkdir(pathWant)
    wavf.write(pathWant + self.string_selected_locatons + '.wav', fs, myrecording)
#################################################
"""
def saveRecording():


    # can use this to specify what folder to put audio in
    #don't use as function just connect to recordsound
    # just see if lines 44-53 work and if not don't worry about it
    fileName = self.string_recording_name
    fs = 44100
    pathWant = os.path.join("../Cardiact/TestSounds/" + fileName)

    # check to see if file already exists
    if os.path.exist(pathWant):
        wavf.write(self.string_recording_name + self.name + '.wav', fs, self.myrecording)
    else:
        os.mkdir(pathWant)
        wavf.write(self.string_recording_name + self.name + '.wav', fs, self.myrecording)

"""

